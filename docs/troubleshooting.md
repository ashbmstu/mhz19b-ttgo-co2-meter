# Troubleshooting

Arranged by what you see, not by what is wrong.

## `Sensor FAIL` on a black screen

The sensor did not answer. In order of likelihood:

- **`RX` and `TX` are swapped.** The board transmits on `GPIO25` into the
  sensor's **RX**, and receives on `GPIO26` from its **TX**. This is the most
  common build fault by a wide margin, and swapping them back does no harm.
- **The sensor is on 3V3.** It needs **5 V**. On 3.3 V it is either silent or
  erratic. See [hardware.md](hardware.md#why-there-is-no-battery).
- **A loose jumper.** Four wires, and the one that comes adrift is usually the
  one with the sensor's weight hanging off it.

The message is printed once at startup and then left alone, so the screen can
say `Sensor FAIL` while the meter is working again. Watch the console instead:
`CO2: read error` every five seconds means it is still not answering.

## The screen is black but the console prints readings

The sensor is fine and the panel is not being driven.

- **The wrong firmware.** If the console shows `ImportError: no module named
  'st7789'` the board has plain MicroPython on it. See
  [flashing.md](flashing.md#what-is-different-about-this-board).
- **A different board revision.** Check `src/tft_config.py` against
  [the display table](hardware.md#the-display).
- **The backlight.** `TFT_BL` is `GPIO4` on this board. If the panel is faintly
  readable under a bright light, that is the backlight and not the driver.

## The display is upside down

Change `TFT_ROTATION` in `src/tft_config.py` from `1` to `3`. They are the same
landscape orientation 180° apart.

## It reads 400 and never moves

Almost always **warm-up**. The first three minutes after power-on are not real
readings. Wait, then breathe gently towards it from 30 cm away and watch it
climb.

If it still does not move after ten minutes, the baseline has been pinned. See
[calibrating by hand](measurement.md#calibrating-by-hand).

## It reads far too low in a room that feels stuffy

The baseline has drifted, or a calibration was run somewhere that was not fresh
air. This is the failure mode worth understanding, because nothing about the
number looks wrong — see [measurement.md](measurement.md#automatic-baseline-correction).

## It reads high and will not come down

Check the sensor is not sealed in. The bay in the printed case is open on
purpose; a sensor in a closed box measures the box.

Also check nothing is breathing on it — a meter at the front of a desk sees
your breath long before it sees the room.

## The reading jumps by a few tens of ppm

Normal. Every reading is drawn as it arrives with no averaging, so the sensor's
own noise is visible. The trend over a minute is the real signal.

## The screen flickers on every update

Also normal. The whole panel is cleared and redrawn every five seconds, which
is visible on an IPS display. It is not a fault and not a loose connection.

## `WiFi...` and then nothing

Only relevant if you set up [publishing](thingspeak.md).

- **2.4 GHz only.** The ESP32 cannot see a 5 GHz network.
- **Check the password** in `config.py`. Fifteen seconds of dots and then
  `Wi-Fi: no connection` on the console means it tried and failed.
- **`Upload rejected`** means the network is fine and ThingSpeak refused the
  update, usually because `UPLOAD_INTERVAL` is below the fifteen seconds a free
  channel allows.

The meter carries on reading and displaying either way. A failed upload never
stops the measurement.

## The board does not appear as a serial port

- **The cable is charge-only.** Many are.
- **The driver is missing.** Depending on the revision the T-Display has a
  CP2104 or a CH9102 USB-serial chip, and Windows needs the matching driver.
- **Nothing is running.** Press Ctrl+C in Thonny's console to interrupt
  `main.py` and get a `>>>` prompt.

## Related

- [flashing.md](flashing.md) — MicroPython and copying the files
- [hardware.md](hardware.md) — wiring diagram and every connection
- [measurement.md](measurement.md) — warm-up, accuracy and calibration
