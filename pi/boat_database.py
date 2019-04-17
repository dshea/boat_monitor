#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 00:25:16 2019

@author: Don Shea
"""
import os
import time
import sqlite3
import json

# database stuff
db_filename = "boat.db"


def openDatabase():
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
        conn = sqlite3.connect(db_filename)
        c = conn.cursor()
    return conn, c

def writeBattery(battery0, battery1, temperature, humidity):
    conn, c = openDatabase()

    # Insert a new row
    c.execute("INSERT INTO battery VALUES (?,?,?,?,?)", 
              (int(time.time()), battery0, battery1, temperature, humidity))

     # Save (commit) the changes
    conn.commit()
    conn.close()

def writeBilge(name, duration) :
    conn, c = openDatabase()
    
    # insert record
    c.execute("INSERT INTO pump VALUES (?,?,?)", 
              (int(time.time()), name, duration))

     # Save (commit) the changes
    conn.commit()
    conn.close()

def makeJSON(time) :
    conn, c = openDatabase()
    
    query =  c.execute('SELECT * FROM pump  WHERE time > ? ORDER BY time', (time,)) 
    print(json.dumps(query))
        

    conn.close()


def dumpDatabase() :
    conn, c = openDatabase()
    
    print("pump database")
    print("time", "name", "duration")
    print("----", "----", "--------")
    for row in c.execute('SELECT * FROM pump ORDER BY time'):
        print(row)

    print("")
    print("battery database")
    print("time", "batery0", "battery1", "temperature", "humidity")
    print("----", "-------", "--------", "-----------", "--------")
    for row in c.execute('SELECT * FROM battery ORDER BY time'):
        print(row)

    conn.close()



if __name__ == '__main__':
#    dumpDatabase()
    makeJSON(1554873300)

    
