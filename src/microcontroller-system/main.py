# -------------------------------------
# IoT Covid-19 Regulation System
# Microcontroller System
# 'main.py'
# Author: Juan Carlos Juárez
# Contact: jc.juarezgarcia@outlook.com
# -------------------------------------

import urequests
import time
import _thread
from hcsr04 import HCSR04
from machine import Pin

# Multi-Threading Functions

def check_total_people():
    global total_people
    while True:
        response = urequests.get(check_total_people_url)
        current_total_people = int(response.text)
        if(total_people != current_total_people):
            print("Total People has changed from: '" + str(total_people) + "' to '" + str(current_total_people) + "'.")
            total_people = current_total_people
        response.close()
        time.sleep(0.2)

def check_max_capacity():
    global max_cap
    while True:
        response = urequests.get(check_max_cap_url)
        current_max_cap = int(response.text)
        if(max_cap != current_max_cap):
            print("Max Capacity has changed from: '" + str(max_cap) + "' to '" + str(current_max_cap) + "'.")
            max_cap = current_max_cap
        response.close()
        time.sleep(0.2)
        

def entrance_detection():
    while True:
        distance = entrance_sensor.distance_cm()
        # Valid Distance
        if(distance < 5): continue
        #print('Distance: ', distance, ' cm')
        if(distance < 70):
            # Send Detection to Back-end Service
            response = urequests.get(entrance_url)
            print(response.status_code)
            response.close()
            # Time for person to move out of sensor sight
            time.sleep(2.5)
        # Time for sensor refreshing
        time.sleep(0.005)

'''
def exit_detection():
    while True:
        distance = exit_sensor.distance_cm()
        # Valid Distance
        if(distance < 5): continue
        #print('Distance: ', distance, ' cm')
        if(distance < 70):
            # Send Detection to Back-end Service
            response = urequests.get(exit_url)
            print(response.status_code)
            response.close()
            # Time for person to move out of sensor sight
            time.sleep(2.5)
        # Time for sensor refreshing
        time.sleep(0.005)
'''
        
# -----------------------------------------------------------

# Main Thread

max_cap = 3

total_people = 0

print("Connected to WLAN.")

entrance_sensor = HCSR04(trigger_pin=23, echo_pin=22, echo_timeout_us=100000)
'''
exit_sensor = HCSR04(trigger_pin=19, echo_pin=18, echo_timeout_us=100000)
'''

check_total_people_url = "http://192.168.1.103:5000/backend-api/check-total-people"
check_max_cap_url = "http://192.168.1.103:5000/backend-api/check-max-capacity"
entrance_url = "http://192.168.1.103:5000/backend-api/entrance"
exit_url = "http://192.168.1.103:5000/backend-api/exit"

# Main Thread Launches Multiple Threads

# Check Total Number of People Thread
_thread.start_new_thread(check_total_people, ())

# Check Max Capacity Thread
_thread.start_new_thread(check_max_capacity, ())

# Entrance Detection Thread
_thread.start_new_thread(entrance_detection, ())

# Exit Detection Thread
'''
_thread.start_new_thread(exit_detection, ())
'''