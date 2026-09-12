# Publishing readings

The meter can post each reading to a **ThingSpeak** channel, which gives you a
chart of the last day or the last month instead of just the last five seconds.
It is free for this sort of use and it needs no server of your own.

**This is off unless you turn it on.** Without a `config.py` on the board the
firmware never imports the networking modules and never switches the radio on.
Nothing is sent, and there is nothing to configure.

## Turning it on

1. **Make an account** at [thingspeak.com](https://thingspeak.com/) and create a
   new channel. *Channels* → *My Channels* → *New Channel*.

2. **Name field 1** something like `CO2` and save. The other fields can stay
   empty.

3. **Copy the Write API Key** from the channel's *API Keys* tab. It is the one
   marked *Write*, not *Read*.

4. **Fill in your own copy of the config.** Take `src/config.example.py`, save
   it as `config.py`, and put your details in:

   ```python
   WIFI_SSID = "your network"
   WIFI_PASS = "your password"

   THINGSPEAK_KEY = "the write key you just copied"
   THINGSPEAK_FIELD = 1

   UPLOAD_INTERVAL = 60
   ```

5. **Upload `config.py` to the board** the same way as the rest — Thonny, right
   click, *Upload to /* — and reset.

The screen shows `WiFi...` with a row of dots while it connects, and after that
a small white square flashes in the bottom corner on every upload. The console
says so too:

```
CO2: 812 ppm | uploaded
CO2: 806 ppm
```

Your chart starts filling up a minute later.

## Turning it off again

Delete `config.py` from the board and reset. You can also just blank out
`THINGSPEAK_KEY`; the firmware only publishes when both the network name and
the key are set.

## Things worth knowing

- **One reading a minute by default.** A free ThingSpeak channel accepts one
  update every 15 seconds, so `UPLOAD_INTERVAL = 60` leaves plenty of room.
  Setting it lower than 15 will get uploads rejected.
- **Nothing is queued.** If the Wi-Fi drops, that minute's reading is lost and
  the next one is tried as normal. The meter keeps working and keeps displaying
  regardless; the upload is the part that is allowed to fail.
- **Only the CO2 number is sent.** One integer, once a minute. No identifiers,
  no location, nothing else.
- **2.4 GHz only.** The ESP32 cannot see a 5 GHz network.

## Keep the key to yourself

`config.py` holds your Wi-Fi password and a key that lets anyone write to your
channel. Two habits worth keeping:

- **It is in `.gitignore` for a reason.** If you fork this repository, do not
  commit your `config.py`. Git remembers a file even after you delete it.
- **The key travels in clear text.** ThingSpeak's simple API is plain HTTP, and
  the key sits in the URL, so anyone on the same network can read it. It is a
  write-only key to one channel, which limits the damage, but do not reuse it
  anywhere else and regenerate it from the *API Keys* tab if you ever paste it
  somewhere public.

## Related

- [flashing.md](flashing.md) — copying files onto the board
- [measurement.md](measurement.md) — what the numbers you are charting mean
