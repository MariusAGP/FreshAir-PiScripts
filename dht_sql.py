#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import board
import sys
import adafruit_dht
import mysql.connector
import datetime
import mh_z19

conn = mysql.connector.connect(host= "sql587.main-hosting.eu",user= "u811821488_admin",passwd="#1Password",db="u811821488_freshair")

c=conn.cursor()

def dhtreading_writesql():
     dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
     humidity = 0
     temperature = 0
     while (humidity == 0):
       humidity = dhtDevice.humidity
       temperature = dhtDevice.temperature
       if (humidity != 0):
         break
     mh_z19_temp = mh_z19.read_all()
     co2 = list(mh_z19_temp.values())[0]

     if humidity is not None and co2 is not None and temperature is not None:
                               print('Temperature={0:0.1f}°C Humidity={1:0.1f}% Co2={2}ppm'.format(temperature, humidity, co2))
     else:
                               print('Failed to get reading. Try again!')
                               sys.exit(1)

     unix = int(time.time())
     date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

     c.execute("INSERT INTO sensordata (temperature, humidity, co2) VALUES (%s, %s, %s)",(temperature, humidity, co2))

     conn.commit()

for i in range(1):
     dhtreading_writesql()

c.close
conn.close()
