#!/usr/bin/python
import sqlite3
import os
import time
import datetime

try:
    db = sqlite3.connect('/home/pi/ELSpring2018/WebAssignment/myTemps.db')
except Error as e:
    print(e)


cursor = db.cursor()
tempfile = open("/sys/bus/w1/devices/28-0000069759e3/w1_slave")
tempfile_text = tempfile.read()

currentTime=time.strftime('%x %X %Z')
tempfile.close()
tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
tempF=tempC*9.0/5.0+32.0
cursor.execute('''INSERT INTO myTemps(currentTime, tempF)
                  VALUES(?,?)''', (currentTime, tempF))
db.commit()
db.close()

