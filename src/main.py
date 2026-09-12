# main.py - CO2 meter on a LILYGO TTGO T-Display with an MH-Z19B sensor.
#
# Reads the sensor over UART every five seconds and redraws the whole panel
# with the reading, a colour and a one-word verdict. Publishing to ThingSpeak
# is optional: it happens only if a config.py exists on the board, and without
# one the radio is never switched on. See docs/thingspeak.md.

import time
from machine import UART

import tft_config
import vga1_8x8 as font

try:
    import config
except ImportError:
    config = None

READ_INTERVAL = 5

# TTGO T-Display V1.1 to MH-Z19B. The pair crosses over: the board transmits
# into the sensor's RX and listens on the sensor's TX.
PIN_TX, PIN_RX = 25, 26
UART_ID = 1
BAUD = 9600

# Automatic baseline correction. The sensor assumes the lowest reading it has
# seen in the last 24 hours was fresh air at 400 ppm, which is true of a room
# that gets aired and false of one that does not. See docs/measurement.md.
ABC_ENABLE = False

GOOD, FAIR = 800, 1200

BLACK = 0x0000
WHITE = 0xFFFF
GREEN = 0x07E0
YELLOW = 0xFFE0
RED = 0xF800

# Rotated into landscape, so the panel's long axis is the one across.
WIDTH = tft_config.TFT_HEIGHT
HEIGHT = tft_config.TFT_WIDTH

WIFI_SSID = getattr(config, "WIFI_SSID", "")
WIFI_PASS = getattr(config, "WIFI_PASS", "")
TS_KEY = getattr(config, "THINGSPEAK_KEY", "")
TS_FIELD = getattr(config, "THINGSPEAK_FIELD", 1)
TS_INTERVAL = getattr(config, "UPLOAD_INTERVAL", 60)
TS_HOST = "api.thingspeak.com"

UPLOAD = bool(WIFI_SSID and TS_KEY)

if UPLOAD:
    import network
    import usocket


def draw_scaled(tft, text, x, y, colour, scale):
    for char in text:
        index = ord(char) - font.FIRST
        if 0 <= index <= font.LAST - font.FIRST:
            glyph = font.FONT[index * 8:(index + 1) * 8]
            for row in range(8):
                for col in range(8):
                    if (glyph[row] >> (7 - col)) & 1:
                        tft.fill_rect(x + col * scale, y + row * scale, scale, scale, colour)
        x += 8 * scale


class MHZ19B:
    def __init__(self, tx, rx):
        self.uart = UART(UART_ID, baudrate=BAUD, tx=tx, rx=rx)

    @staticmethod
    def _checksum(frame):
        return (0xFF - sum(frame[1:8]) % 256 + 1) & 0xFF

    def read(self):
        self.uart.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
        time.sleep(0.1)
        reply = self.uart.read(9)
        if reply and len(reply) == 9 and reply[8] == self._checksum(reply):
            return reply[2] * 256 + reply[3]
        return None

    def set_abc(self, enable):
        # The sensor sends no reply to this command and offers no way to read
        # the setting back, so it is written on every boot rather than checked.
        frame = bytearray([0xFF, 0x01, 0x79, 0xA0 if enable else 0x00, 0, 0, 0, 0, 0])
        frame[8] = self._checksum(frame)
        self.uart.write(frame)
        time.sleep(0.1)


def connect_wifi(tft):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        for attempt in range(15):
            if wlan.isconnected():
                break
            time.sleep(1)
            draw_scaled(tft, ".", 10 + attempt * 10, 10, WHITE, 2)
    if wlan.isconnected():
        print("Wi-Fi:", wlan.ifconfig()[0])
        return True
    print("Wi-Fi: no connection")
    return False


def send_to_thingspeak(ppm):
    try:
        address = usocket.getaddrinfo(TS_HOST, 80)[0][-1]
        sock = usocket.socket()
        sock.settimeout(5)
        sock.connect(address)
        sock.write(f"GET /update?api_key={TS_KEY}&field{TS_FIELD}={ppm} "
                   f"HTTP/1.1\r\nHost: {TS_HOST}\r\nConnection: close\r\n\r\n")
        status = sock.readline()
        sock.close()
        if b"200" in status:
            return True
        print("Upload rejected:", status)
    except Exception as error:
        print("Upload failed:", error)
    return False


def band(ppm):
    if ppm < GOOD:
        return GREEN, "GOOD"
    if ppm < FAIR:
        return YELLOW, "FAIR"
    return RED, "POOR"


def draw(tft, ppm):
    colour, status = band(ppm) if ppm else (WHITE, "Wait")
    reading = str(ppm) if ppm else "----"

    tft.fill(BLACK)
    draw_scaled(tft, "CO2 Level:", 10, 5, WHITE, 2)
    tft.fill_rect(WIDTH - 30, 5, 20, 20, colour)

    scale = 5
    x = (WIDTH - len(reading) * 8 * scale) // 2
    draw_scaled(tft, reading, x, 40, colour, scale)

    draw_scaled(tft, "ppm", WIDTH - 60, 90, WHITE, 2)
    draw_scaled(tft, status, 10, 100, colour, 3)


def main():
    tft = tft_config.config()
    tft.init()
    tft.fill(BLACK)

    sensor = MHZ19B(PIN_TX, PIN_RX)
    if sensor.read() is None:
        print("Sensor: no reply")
        draw_scaled(tft, "Sensor FAIL", 10, 10, RED, 2)
    else:
        print("Sensor: ok")
        draw_scaled(tft, "Sensor OK", 10, 10, GREEN, 2)
    time.sleep(1)

    sensor.set_abc(ABC_ENABLE)
    print("ABC:", "on" if ABC_ENABLE else "off")

    if UPLOAD:
        tft.fill(BLACK)
        draw_scaled(tft, "WiFi...", 10, 10, WHITE, 2)
        connect_wifi(tft)

    last_upload = 0

    while True:
        ppm = sensor.read()
        print(f"CO2: {ppm} ppm" if ppm else "CO2: read error", end="")
        draw(tft, ppm)

        now = time.time()
        if UPLOAD and ppm and now - last_upload >= TS_INTERVAL:
            tft.fill_rect(WIDTH - 10, HEIGHT - 10, 5, 5, WHITE)
            if not network.WLAN(network.STA_IF).isconnected():
                connect_wifi(tft)
            print(" | uploaded" if send_to_thingspeak(ppm) else " | upload failed", end="")
            last_upload = now

        print("")
        time.sleep(READ_INTERVAL)


if __name__ == "__main__":
    main()
