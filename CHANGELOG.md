# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-12

First public release. The meter has been running on a desk since January 2026;
this is the point at which somebody else could build one.

### Added

- **A carbon dioxide reading on a 135 × 240 IPS panel**, drawn large enough to
  read across a room, with a colour band and a one-word verdict so that it can
  be understood without being read.
- **A driver for the MH-Z19B** over its UART: the nine-byte command frame, the
  checksum on the reply, and the automatic baseline correction setting.
- **Optional publishing to ThingSpeak.** Off unless a `config.py` is present on
  the board, in which case the meter joins a network and posts the reading once
  a minute. Without that file the networking modules are never imported and the
  radio is never switched on.
- **Documentation for the whole build**: [flashing](docs/flashing.md), which
  covers the display driver being compiled into the firmware rather than copied
  onto the board; [hardware](docs/hardware.md) with a wiring diagram;
  [measurement](docs/measurement.md) on warm-up, baseline drift and calibrating
  by hand; [publishing](docs/thingspeak.md); and symptom-first
  [troubleshooting](docs/troubleshooting.md).
- **A CI check that the pin numbers agree** across `src/main.py`,
  `src/tft_config.py`, `docs/hardware.md` and the wiring diagram. The two data
  pins cross over between the board and the sensor, and that pairing is asserted
  rather than inferred, so a documentation edit that quietly un-crosses them
  fails the build.

### Changed

- **Credentials come from a `config.py` that is not in this repository**, rather
  than from constants in the firmware. `src/config.example.py` shows what goes
  in it, and `.gitignore` keeps the real one out of git.
- **The font is a file rather than a string.** Previously the firmware carried
  an 8 × 8 font as a literal and wrote it to the filesystem at boot if it was
  missing, which removed about 3.8 KB of unreadable text from the top of
  `main.py`. It ships as `src/vga1_8x8.py` instead: the VGA font file from
  st7789_mpy, the same module the prebuilt firmware already has frozen in. The
  old literal turned out to be a different, unattributed glyph set with a
  damaged lower-case block, so the digits now have the VGA shapes and the
  `ppm` label renders properly.
- **Panel dimensions and rotation come from `tft_config.py`** instead of being
  repeated as literals in the drawing code, which had the rotation set in two
  places with two different values.
- Dropped four imports that nothing used.
