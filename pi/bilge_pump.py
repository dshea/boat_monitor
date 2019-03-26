#!/usr/bin/env python3

from gpiozero import Button, LED
from signal import pause
from time import time, ctime

bilgePump1Pin = 13
bilgePump2Pin = 19
led1Pin = 18

class BilgePump(Button):
    """A class to track the bilge pump cycling"""

    def __init__(self, name, pin, alert=False):
        super(). __init__(pin)
        self.name = name
        self.alert = alert
        self.onTime = time()
        self.when_pressed = self.pumpOn
        self.when_released = self.pumpOff

    def pumpOn(self):
        print(self.name, "- ON")
        if self.alert:
            print("**** Send a text message to Don since this is pump", self.pin.number)
        self.onTime = time()

    def pumpOff(self):
        print(self.name, "- OFF")
        offTime = time()
        delta = offTime - self.onTime
        print(ctime(offTime), "- pump", self.pin.number, ", duration =", delta)




bilgePump1 = BilgePump("Main (small)", bilgePump1Pin)
bilgePump2 = BilgePump("Backup (big)", bilgePump2Pin, True)
led1 = LED(led1Pin)

led1.source = bilgePump1



pause()

