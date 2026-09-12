# Measurement

What the number means, how far to trust it, and how to correct it when it
drifts.

## What the sensor actually does

The MH-Z19B is an **NDIR** sensor: non-dispersive infrared. A small lamp shines
through a gold-plated tube full of room air onto a detector tuned to the
wavelength carbon dioxide absorbs. More CO2 in the tube, less light arrives.
There is no chemistry to wear out and nothing to replace, which is why a sensor
like this outlasts the cheap electrochemical parts sold for the same job.

What it cannot do is tell you about any other gas. It does not detect carbon
**monoxide**, smoke, solvents, cooking fumes or anything else. A CO2 reading of
500 ppm in a room filling with CO is still 500 ppm.

## Warm-up

**The first three minutes are meaningless.** The lamp and the detector have to
reach a stable temperature, and until they do the sensor reports whatever its
last calibration left behind — very often a flat 400 or 515 ppm.

Plug the meter in, walk away, and come back. If you are testing a build, that
is the difference between a sensor that is broken and one that is simply cold.

## Reading the number

CO2 indoors is mostly you, breathing. Treated as a ventilation gauge rather
than a pollutant measurement, it is one of the most useful numbers you can put
on a desk.

| ppm | On screen | What it means |
|---|---|---|
| **400 – 600** | `GOOD` | Outdoor air, or a room with a window open |
| **600 – 800** | `GOOD` | Normal occupied room. Nothing to do |
| **800 – 1200** | `FAIR` | Ventilation is falling behind the people in the room |
| **1200 – 2000** | `POOR` | Noticeably close. This is the range where people report headaches and dullness |
| **2000 +** | `POOR` | Open something |

The two thresholds are `GOOD` and `FAIR` at the top of `src/main.py`. They are
a judgement, not a standard — move them if your own experience of a room
disagrees.

## How accurate is it

The datasheet claims **±(50 ppm + 5% of the reading)**. At 1000 ppm that is
±100 ppm, which is plenty for deciding whether to open a window and nowhere
near enough to publish.

Two things matter more than that specification in practice:

- **The baseline.** Everything below depends on the sensor knowing what fresh
  air looks like. A mis-set baseline shifts every reading by the same amount,
  and nothing about the number on screen will look wrong.
- **Air pressure.** NDIR sensors read the number of molecules in the tube, so
  the same air measured at altitude or in a deep low-pressure system reads
  lower. There is no pressure compensation in this part and none in this
  firmware. It is worth knowing about if you live high up; at sea level ignore
  it.

## Testing that it works

Breathe gently towards the sensor from about 30 cm away — not into it, which
saturates it for a while. The reading should climb within a few seconds and
fall back over a minute or two. A sensor that does not move is not reading.

The decay is as informative as the spike. A room that clears in a minute has
real air movement; one that takes ten minutes does not.

## Automatic baseline correction

The sensor can correct its own drift. Every 24 hours, ABC takes the **lowest
reading it has seen** in that period and decides that this was fresh air at
400 ppm.

That works beautifully in a room that gets aired, and fails quietly in a room
that does not. A bedroom kept shut, a small office, a workshop in winter — none
of them may ever reach outdoor air, so the sensor pins its baseline to
whatever the quietest hour of the night happened to be, and everything after
that reads low.

**This firmware turns ABC off**, in `src/main.py`:

```python
ABC_ENABLE = False
```

The command is sent on every boot, because the sensor sends no reply to it and
offers no way to read the setting back.

Turning it off means drift is yours to correct. Over months, expect the reading
to wander. If your meter lives in a room with a window that gets opened, set
`ABC_ENABLE = True` instead and let the sensor look after itself — that is the
easier life, and for most rooms it is the right answer.

## Calibrating by hand

If ABC is off, or if the reading has clearly settled somewhere wrong, you can
set the baseline yourself. The sensor treats this as "the air around me now is
400 ppm", so everything depends on the air actually being outdoor air.

1. Take the meter outside, or to an open window with a breeze, and leave it
   powered for **at least 20 minutes**. Not next to yourself, a car, or a
   flue.
2. Connect the sensor's **HD** pin to **GND** and hold it there for **more than
   seven seconds**.
3. Disconnect it. The baseline is now 400 ppm.

A useful check afterwards: outdoor air away from traffic is 400 to 450 ppm
almost everywhere on earth. If your meter reads that outside and climbs
sensibly indoors, it is working.

## What it does not do

- **No logging and no clock.** The meter shows the present moment. If you want a
  record, [thingspeak.md](thingspeak.md) is the small version of that.
- **No averaging.** Every five seconds it draws the latest reading, so the
  display twitches by a few tens of ppm. That is the sensor's noise, not the
  room changing.
- **No humidity or temperature.** The MH-Z19B has no such output.

## Related

- [hardware.md](hardware.md) — the sensor's other pins, including `HD`
- [thingspeak.md](thingspeak.md) — optional: charting the readings over time
- [troubleshooting.md](troubleshooting.md) — when the number looks wrong
