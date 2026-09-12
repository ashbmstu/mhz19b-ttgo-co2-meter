# Contributing to mhz19b-ttgo-co2-meter

Thank you for considering a contribution. This is a small piece of MicroPython
for a specific pair of parts, and most changes to it only mean anything on a
real board with a real sensor attached.

## Before you open a pull request

There is no simulator. CI checks that the files parse, that the pin numbers
agree across the code, the wiring table and the diagram, and that the links in
the documentation resolve. It cannot talk to a sensor or light a panel.
Anything past that has to be tried on hardware.

If your change touches the measurement path, say in the pull request what you
saw before and after, and under what conditions. A reading taken alongside a
reference instrument, or a breathe-and-decay curve, is worth far more than an
argument about the arithmetic. Say how long the sensor had been warm, too —
three minutes of warm-up explains a surprising number of strange readings.

## Running the checks locally

```bash
python -m compileall -q src tools
python tools/check-pins.py
```

## Code style

- MicroPython, 4-space indent, no tabs.
- `snake_case` for functions and variables.
- Match the style of `src/main.py`.
- Comments explain why, not what. Most of this code needs none.
- Catch `Exception`, not a bare `except:`. A bare except swallows Ctrl+C, which
  makes a board running a tight sensor loop very tedious to interrupt.

## Credentials

Never commit a `config.py`. It is in `.gitignore`, it holds a Wi-Fi password and
a ThingSpeak write key, and git remembers a file long after it is deleted. The
same goes for a screenshot of a console with a key in it.

## Commit messages

Use an imperative subject line under about 72 characters, with no type prefix.
In the body, explain the reasoning. When a change comes from something you
measured, say what you measured and with what.

## Reporting a problem with a meter you built

Useful reports include:

- What the panel shows, and what the serial console prints every five seconds
- How long it had been powered on when you looked
- MicroPython version and which firmware image you flashed (`import sys;
  sys.implementation` at the REPL)
- Which T-Display revision, and the range marked on your MH-Z19B
- Whether the same thing happens with the sensor out of the case

Open bugs through GitHub Issues on this repository.
