# tft_config.py - how the ST7789 panel is wired to the ESP32 on a TTGO
# T-Display V1.1. Nothing here needs soldering; the panel is on the board.

import machine
import st7789

# The panel is 1.14 inch and 135 x 240. The ST7789V can address 240 x 320, but
# not on this board.
TFT_WIDTH = 135
TFT_HEIGHT = 240

TFT_MOSI = 19
TFT_SCLK = 18
TFT_CS = 5
TFT_DC = 16
TFT_RST = 23
TFT_BL = 4

# Landscape. 1 and 3 are the same orientation 180 degrees apart, so if the
# reading comes out upside down in your case, swap this for the other one.
TFT_ROTATION = 1

BAUDRATE = 30000000


def config():
    spi = machine.SPI(1, baudrate=BAUDRATE,
                      sck=machine.Pin(TFT_SCLK),
                      mosi=machine.Pin(TFT_MOSI))
    return st7789.ST7789(
        spi,
        TFT_WIDTH,
        TFT_HEIGHT,
        reset=machine.Pin(TFT_RST, machine.Pin.OUT),
        cs=machine.Pin(TFT_CS, machine.Pin.OUT),
        dc=machine.Pin(TFT_DC, machine.Pin.OUT),
        backlight=machine.Pin(TFT_BL, machine.Pin.OUT),
        rotation=TFT_ROTATION,
    )
