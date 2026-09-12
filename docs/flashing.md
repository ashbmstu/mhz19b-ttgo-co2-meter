# Flashing

Two stages: put MicroPython on the board once, then copy four files onto it.
About fifteen minutes the first time, a few seconds every time after that.

## What is different about this board

The display is driven by a **C module called `st7789`**, which is compiled into
the firmware rather than copied on as a Python file. The plain MicroPython
download from micropython.org does not have it, and the meter will stop at
`ImportError: no module named 'st7789'`.

So instead of the usual firmware, use one of the prebuilt images from
[russhughes/st7789_mpy](https://github.com/russhughes/st7789_mpy). The
`firmware` directory there has a build for this board under **`T-DISPLAY`**.
Download `firmware.bin` from that folder.

## Stage one: MicroPython

**You need** a USB cable that carries data, not just power, and Python on your
computer.

1. **Install the USB driver** if the board does not appear as a serial port.
   Depending on the revision the T-Display has a CP2104 or a CH9102 chip; the
   driver is a download from Silicon Labs or WCH respectively. On Linux it is
   already there.

2. **Install esptool:**

   ```bash
   pip install esptool
   ```

3. **Find the port.** `COM3`, `COM7` and so on on Windows; `/dev/ttyUSB0` on
   Linux; `/dev/cu.usbserial-*` on macOS. Unplug the board and plug it back in
   to see which name appears.

4. **Erase the flash.** Substitute your own port here and below.

   ```bash
   esptool.py --chip esp32 --port COM3 erase_flash
   ```

5. **Write the firmware**, from the folder you downloaded it into:

   ```bash
   esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 firmware.bin
   ```

If esptool says it cannot connect, hold the **BOOT** button down while the
command starts, and let go once it says `Connecting...`.

## Stage two: the files

1. **Install [Thonny](https://thonny.org/).** It is a small Python editor that
   can read and write the board's filesystem, and it is the least fiddly way to
   do this.

2. **Point it at the board.** *Run* → *Configure interpreter* → **MicroPython
   (ESP32)**, then pick the port. The bottom pane should turn into a `>>>`
   prompt. Press Ctrl+C there if it does not.

3. **Copy the files.** *View* → *Files* gives you your computer on top and the
   board underneath. Take the four files from `src/` and, for each one,
   right-click → **Upload to /**:

   ```
   main.py
   tft_config.py
   vga1_8x8.py
   ```

   `config.example.py` stays on your computer unless you want the meter to
   publish readings — see [thingspeak.md](thingspeak.md).

   They must land in the board's root, not in a folder. MicroPython runs
   `/main.py` at boot and looks nowhere else.

4. **Reset the board** with the button next to the USB socket, or unplug it and
   plug it back in.

The screen shows `Sensor OK`, then a reading about five seconds later. The
console prints one line every five seconds:

```
Sensor: ok
ABC: off
CO2: 812 ppm
CO2: 806 ppm
```

**The first few minutes are not real.** The sensor needs about three minutes to
warm up, and the readings before that mean nothing. See
[measurement.md](measurement.md).

## Changing the code

Edit the file in Thonny and upload it again, or open the copy on the board
directly and save with Ctrl+S. Either way, reset the board afterwards. Ctrl+C in
the console stops the running program so you can get a `>>>` prompt back.

## Why the font is a file

The prebuilt firmware above already has font modules frozen into it, so
`vga1_8x8` would import even if you did not copy it. It is included here anyway
so that the meter also runs on a firmware you built yourself, and so that the
repository is the whole story.

## Related

- [hardware.md](hardware.md) — what connects to what
- [troubleshooting.md](troubleshooting.md) — when the above does not happen
