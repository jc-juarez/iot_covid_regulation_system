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
from LCD import CharLCD
import dht

# Multi-Threading Functions

def check_total_people():
    global total_people
    global max_cap
    while True:
        response = urequests.get(check_total_people_url)
        current_total_people = int(response.text)
        if(total_people != current_total_people):
            print("Total People has changed from: '" + str(total_people) + "' to '" + str(current_total_people) + "'.")
            total_people = current_total_people
        response.close()
        time.sleep(0.2)
        
def check_temperature():
    global total_people
    global max_cap
    global thread_blocker
    global seen_temperature
    while True:
        if(total_people >= max_cap):
            lcd.set_line(0)
            lcd.message('Sorry!', 2)
            lcd.set_line(1)
            lcd.message('Full Capacity.', 2)
        else:
            # Check for temperature
            # if enters a range call function
            # Change False for condition to check
            # valid high temperature range
            temperature_sensor.measure()
            curr_temperature = temperature_sensor.temperature()
            print(curr_temperature)
            if(curr_temperature > 20):
                # If temperature is too high deny entry
                if(curr_temperature > 30):
                    # Call endpoint for entry denial
                    lcd.set_line(0)
                    lcd.message('High Temp!', 2)
                    lcd.set_line(1)
                    lcd.message('Entry Denied.', 2)
                    time.sleep(5)
                    pass
                else:
                    seen_temperature = curr_temperature
                    thread_blocker = True
                    while(thread_blocker):
                        lcd.set_line(0)
                        lcd.message('OK. Your Temp:', 2)
                        lcd.set_line(1)
                        lcd.message(str(curr_temperature), 2)
            else:
                lcd.set_line(0)
                lcd.message('Welcome', 2)
                lcd.set_line(1)
                lcd.message('Check Temp.', 2)

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
    global seen_temperature
    global thread_blocker
    while True:
        distance = entrance_sensor.distance_cm()
        # Valid Distance
        if(distance < 5): continue
        print('Distance: ', distance, ' cm')
        if(distance < 50):
            # Send Detection to Back-end Service along with
            # the seen temperature
            response = urequests.get(entrance_url)
            print(response.status_code)
            response.close()
            thread_blocker = False
            seen_temperature = 0
            # Time for person to move out of sensor sight
            print("Person in...")
            time.sleep(2.5)
        # Time for sensor refreshing
        time.sleep(0.005)

def exit_detection():
    while True:
        distance = exit_sensor.distance_cm()
        # Valid Distance
        if(distance < 5): continue
        #print('Distance2: ', distance, ' cm')
        if(distance < 50):
            # Send Detection to Back-end Service
            response = urequests.get(exit_url)
            print(response.status_code)
            response.close()
            # Time for person to move out of sensor sight
            time.sleep(2.5)
        # Time for sensor refreshing
        time.sleep(0.005)

        
# -----------------------------------------------------------

# Main Thread

lcd = CharLCD(rs=2, en=4, d4=15, d5=13, d6=12, d7=14, cols=16, rows=2)

max_cap = 3

total_people = 0

thread_blocker = False

seen_temperature = 0

print("Connected to WLAN.")

entrance_sensor = HCSR04(trigger_pin=23, echo_pin=22, echo_timeout_us=100000)

exit_sensor = HCSR04(trigger_pin=19, echo_pin=18, echo_timeout_us=100000)

temperature_sensor = dht.DHT11(Pin(25))

check_total_people_url = "http://172.20.10.3:5000/backend-api/check-total-people"
check_max_cap_url = "http://172.20.10.3:5000/backend-api/check-max-capacity"
entrance_url = "http://172.20.10.3:5000/backend-api/entrance"
exit_url = "http://172.20.10.3:5000/backend-api/exit"

# Main Thread Launches Multiple Threads

# Check Total Number of People Thread
_thread.start_new_thread(check_total_people, ())

# Check Max Capacity Thread
_thread.start_new_thread(check_max_capacity, ())

# Entrance Detection Thread
_thread.start_new_thread(entrance_detection, ())

# Exit Detection Thread
_thread.start_new_thread(exit_detection, ())

# Temperature Checking Thread
_thread.start_new_thread(check_temperature, ())
