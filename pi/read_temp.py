#!/usr/bin/env python3

import sys
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 5


while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # convert to fehrenheit
    temperature = temperature * 9.0/5.0 + 32.0

    print("temp=%.1f, humidity=%.1f" % (temperature, humidity))

    time.sleep(2)
