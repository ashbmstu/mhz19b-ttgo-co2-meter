# Security

This is a carbon dioxide meter built from a development board and a sensor. It
runs on a desk, from a USB cable, and there is not much of an attack surface to
speak of. Two things are nevertheless worth taking seriously.

## Credentials

The meter can optionally publish readings to ThingSpeak, and doing so means
putting a Wi-Fi password and a channel write key on the board in a `config.py`.
That file is in `.gitignore` and there are no credentials anywhere in this
repository. If you ever find one that has crept in — in a commit, in an issue,
in a screenshot in the documentation — please report it rather than opening a
pull request, so that it can be revoked before it is pointed at.

Two properties of the upload are worth knowing rather than reporting, because
they are how the service works rather than defects here:

- The request is plain HTTP and the key travels in the URL, so anyone on the
  same network can read it. It is a write-only key for one channel.
- Channel data is as public or private as you configure the channel to be. The
  firmware sends one integer and no identifiers.

## Measurement

**A measurement bug is the way this project can do actual harm.** A meter that
reads low tells somebody a room is fine when it is not. A misparsed frame that
returns a stale value, a baseline pinned to the wrong number, a checksum check
that passes when it should not — any of those leave a person sitting in a room
they would otherwise have ventilated, with no sign on the display that anything
is wrong. Treat that as a safety issue and report it, even though none of it is
a security vulnerability in the ordinary sense.

This is a hobby instrument. It is not a workplace exposure monitor, not an
alarm, and not a medical device, and it must not be relied on as one.

It cannot detect carbon **monoxide**, which is the gas that kills people in
homes. Buy a certified CO alarm for that.

## How to report

Use [GitHub's private vulnerability
reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
on this repository. For an ordinary measurement bug a normal issue is fine and
easier to discuss in the open.

## What to expect

There is no support commitment and no CVE process. Reports are read in good
faith; fixes depend on maintainer time and on how badly the bug misleads.
