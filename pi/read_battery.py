#!/usr/bin/env python3

import time
import os
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import Adafruit_DHT
import sqlite3

# battery calibration
#
# assume adc reading is 0 when battery voltage is 0
#
# batteryVoltage = adcReading * ratio
#
adc0_voltage = 2.8
battery0_voltage = 12.5
battery0_ratio = battery0_voltage / adc0_voltage 

adc1_voltage = 2.8
battery1_voltage = 12.5
battery1_ratio = battery1_voltage / adc1_voltage 

battery_num_readings = 5

# what pin is the temp sensor attached to
temperature_pin = 5
temperature_num_readings = 5

# database stuff
db_filename = "boat.db"


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)

chan0_sum = 0.0
chan1_sum = 0.0

# read the battery ADC a few times
for i in range(battery_num_readings):
    chan0_sum += chan0.voltage
    chan1_sum += chan1.voltage
    time.sleep(0.1)
    
battery0 = (chan0_sum / battery_num_readings) * battery0_ratio
battery1 = (chan1_sum / battery_num_readings) * battery1_ratio

print("battery0=%.2f, battery1=%.2f" % (battery0, battery1))

#
# now for the temp and humidity
#
sensor = Adafruit_DHT.DHT11

temperature_sum = 0.0
humidity_sum = 0.0
count = 0

for i in range(temperature_num_readings):
    h, t = Adafruit_DHT.read_retry(sensor, temperature_pin)
    if (h != None) and (t != None):
        count += 1
        temperature_sum += t
        humidity_sum += h
    time.sleep(0.1)

# convert to fehrenheit
temperature = (temperature_sum / count) * 9.0/5.0 + 32.0
humidity = humidity_sum / count

print("temp=%.1f, humidity=%.1f" % (temperature, humidity))


#
# OK, now write to the database
#
conn = None
if not os.path.isfile(db_filename):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    
    # Create table pump
    c.execute('''CREATE TABLE pump
             (time INT, name text, duration INT)''')

    # Create table battery
    c.execute('''CREATE TABLE battery
             (time INT, battery0 REAL, battery1 REAL, 
             temperature REAL, humidity REAL)''')
    
    conn.commit()
else:
    c = conn.cursor()
    conn = sqlite3.connect(db_filename)
    
# Insert a new row
c.execute("INSERT INTO battery VALUES (?,?,?,?,?)", 
          (int(time.time()), battery0, battery1, temperature, humidity))

 # Save (commit) the changes
conn.commit()
conn.close()

  
    
