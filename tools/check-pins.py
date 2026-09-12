#!/usr/bin/env python3
"""Check that the code, the wiring table and the diagram agree about pins.

Two GPIO numbers carry the only wires that anyone has to solder, and they are
written down in three places: the constants in src/main.py, the wiring table in
docs/hardware.md, and the labels in docs/img/wiring.svg.

They cross over. The board transmits on PIN_TX into the sensor's RX, and
receives on PIN_RX from its TX, so a table that lines PIN_TX up against the
sensor's TX is wrong in the way that is hardest to see and costs the most time
on the bench. That pairing is asserted below rather than inferred.

The six display pins are checked too. Nothing is soldered for the panel, but
src/tft_config.py has to match whichever board revision is in front of you, and
the table is where somebody will look first.
"""

import ast
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Constant in main.py -> the (device, pin) it lands on in the wiring table.
CONSTANTS = {
    "PIN_TX": ("MH-Z19B", "RX"),
    "PIN_RX": ("MH-Z19B", "TX"),
}

# Constant in tft_config.py -> the signal named in the display table.
DISPLAY = {
    "TFT_MOSI": "MOSI",
    "TFT_SCLK": "SCLK",
    "TFT_CS": "CS",
    "TFT_DC": "DC",
    "TFT_RST": "RST",
    "TFT_BL": "BL",
}


def assignments(path, wanted):
    """Pull integer constants out of a module, including tuple assignments."""
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            names, values = [target], [node.value]
            if isinstance(target, ast.Tuple) and isinstance(node.value, ast.Tuple):
                names, values = target.elts, node.value.elts
            for name, value in zip(names, values):
                if (isinstance(name, ast.Name) and name.id in wanted
                        and isinstance(value, ast.Constant)):
                    found[wanted[name.id]] = value.value
    return found


def rows():
    """Every three-cell table row in hardware.md whose last cell is a GPIO."""
    text = (ROOT / "docs" / "hardware.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and re.fullmatch(r"GPIO\d+", cells[2].strip("`")):
            yield cells, int(cells[2].strip("`")[4:])


def from_table():
    found = {}
    for cells, gpio in rows():
        signal = re.search(r"`([^`]+)`", cells[0])
        pad = re.search(r"`([^`]+)`", cells[1])
        if not signal or not pad:
            continue
        key = (("MH-Z19B", signal.group(1)) if "MH-Z19B" in cells[0]
               else signal.group(1))
        found[key] = (pad.group(1), gpio)
    return found


def from_diagram():
    """Collect the GPIO numbers labelled in the diagram.

    Only the set is compared, not the pairing. Tying the check to the exact
    coordinates of each label would break every time the diagram is redrawn,
    which is a worse failure than the one it would catch; the table above
    already pins down which signal goes where.
    """
    svg = ET.parse(ROOT / "docs" / "img" / "wiring.svg")
    labels = [el.text.strip() for el in svg.iter()
              if el.tag.endswith("text") and el.text]
    return {int(m.group(1)) for t in labels
            for m in [re.match(r"GPIO(\d+)$", t)] if m}


def compare(code, table, problems, label):
    for key, gpio in sorted(code.items(), key=lambda kv: str(kv[0])):
        where = " ".join(key) if isinstance(key, tuple) else f"display {key}"
        if key not in table:
            problems.append(f"{where}: missing from docs/hardware.md")
            continue
        pad, said = table[key]
        if said != gpio:
            problems.append(
                f"{where}: {label} says GPIO{gpio}, docs/hardware.md says GPIO{said}")
        if pad.strip("IO") != str(said):
            problems.append(f"{where}: docs/hardware.md pairs pad {pad} with GPIO{said}")


def main():
    wires = assignments(Path("src") / "main.py", CONSTANTS)
    display = assignments(Path("src") / "tft_config.py", DISPLAY)
    table = from_table()
    problems = []

    for name, key in CONSTANTS.items():
        if key not in wires:
            problems.append(f"{' '.join(key)}: no {name} in src/main.py")
    for name, key in DISPLAY.items():
        if key not in display:
            problems.append(f"display {key}: no {name} in src/tft_config.py")

    compare(wires, table, problems, "src/main.py")
    compare(display, table, problems, "src/tft_config.py")

    diagram = from_diagram()
    if diagram != set(wires.values()):
        problems.append(
            f"docs/img/wiring.svg labels GPIOs {sorted(diagram)}, "
            f"but src/main.py wires {sorted(set(wires.values()))}")

    if problems:
        print("Pin definitions disagree:")
        for problem in problems:
            print("  " + problem)
        return 1

    for (device, signal), gpio in sorted(wires.items()):
        print(f"{device} {signal}: GPIO{gpio} - code, table and diagram agree")
    for signal, gpio in sorted(display.items()):
        print(f"display {signal}: GPIO{gpio} - code and table agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
