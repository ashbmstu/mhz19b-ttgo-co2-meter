# Optional. Copy this file onto the board as config.py and fill it in to have
# the meter publish to ThingSpeak. Leave it off the board and the meter runs
# offline: the radio is never switched on. See docs/thingspeak.md.
#
# config.py is in .gitignore. Keep it that way - the write key below is a
# credential.

WIFI_SSID = ""
WIFI_PASS = ""

# The Write API Key from your channel's "API Keys" tab, and the number of the
# field to write the reading into.
THINGSPEAK_KEY = ""
THINGSPEAK_FIELD = 1

# Seconds between uploads. A free ThingSpeak channel accepts one every 15.
UPLOAD_INTERVAL = 60
