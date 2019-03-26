#!/usr/bin/env python3

from gpiozero import Button, LED
from signal import pause
from time import sleep


button1Pin = 19
led1Pin = 18

led1 = LED(led1Pin)

while True:
	led1.on()
	sleep(1)
	led1.off()
	sleep(5)

