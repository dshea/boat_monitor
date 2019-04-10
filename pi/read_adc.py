#!/usr/bin/env python3

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)

print("{:>5}\t{:>5}\t{:>5}".format('raw0', 'v0', 'v1'))

while True:
    print("{:>5}\t{:>5.3f}\t{:>5.3f}".format(chan0.value, chan0.voltage, chan1.voltage))
    time.sleep(0.1)

