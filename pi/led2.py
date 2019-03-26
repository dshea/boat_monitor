#!/usr/bin/env python3

from gpiozero import Button, LED
from signal import pause


button1Pin = 19
led1Pin = 18

button1 = Button(button1Pin)
led1 = LED(led1Pin)

led1.source = button1

pause()

