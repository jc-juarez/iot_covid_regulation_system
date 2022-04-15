# -------------------------------------
# IoT Covid-19 Regulation System
# Microcontroller System
# 'boot.py'
# Author: Juan Carlos Juárez
# Contact: jc.juarezgarcia@outlook.com
# -------------------------------------

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

# Use your WLAN credentials here
ssid = '************'
password = '************'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connected.')
print(station.ifconfig())