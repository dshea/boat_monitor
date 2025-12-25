# boat_monitor
Raspberry pi and website code to monitor Nightshade's bilge pumps and batteries

## raspberry pi data collection

    - init startTime = stopTime = currentTime
    - init pumpState = off
    - init messageSent = false
    - loop
        - newState = read pump state
        - if newState != pumpState
            - pumpState = newState
            - if pumpState == on
                - startTime = currentTime
            - else (pump turned off)
                - duration = currentTime - startTime
                - stopTime = currentTime
                - save database record
                - messageSent = false
        - else (state is the same)
            - if pumpState == on
                - if !messageSent
                    - duration = currentTime - startTime
                    - if duration > maxOnTime
                        - send warning text / email
                        - messageSent = true
        - delay 1 sec

## raspberry pi upload

    - upload jason file 4x? a day
        - read database and create json file
	- use web page with php to transfer file
    - file name = 2019-03-28T15:53:00.json
	- php should read new json file and load into database
    - php web page should make updated csv file for the graphing page
      from database, so the graph data is static.

## web php
    - create graph from static data file
    - display graph in browser
	- plotly.js

## database fields

pump
    - time - (int) unixtime pump turned on
    - name - (str) pump name
    - duration - (int) # seconds pump was on

battery
    - time - (int) unixtime reading was taken
    - battery1 - (float) battery bank 1, house bank
    - battery2 - (float) battery bank 2, starting battery
    - temp - (float) temp in fahrenheit
    - humidity - (float) precent relative humidity

## raspberry pi hardware

DHT22 temp humidity sensor
    - https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/wiring
    - sudu pip3 install adafruit-circuitpython-dht
    - sudo apt-get install libgpiod2
    - wire data to GPIO pin 4

ADS1115 16bit Analog to digital converter 4 channel
    - https://learn.adafruit.com/adafruit-4-channel-adc-breakouts
    - enable i2c in raspi-config
    - sudo pip3 install adafruit-circuitpython-ads1x15

    