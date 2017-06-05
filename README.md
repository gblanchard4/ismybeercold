# ismybeercold.com
Checking the temp on my beer using technology!

## Whats used
This project uses a Raspberry Pi and a DS18B20 sensor
I am using http://Resin.io to deliver the project to the Pi.

## Instructions

### Enabling 1Wire Support
From: https://docs.resin.io/hardware/i2c-and-spi/#1-wire-and-digital-temperature-sensors

Need to edit `config.txt` on the `resin-boot` partition of the SD card
and add the line `dtoverlay=w1-gpio`

Need to add `modprobe w1-gpio && modprobe w1-therm` in our  Dockerfile `CMD` command
