# -------------------------------------
# IoT Covid-19 Regulation System
# Front-end App
# 'app.py'
# Author: Juan Carlos Juárez
# Contact: jc.juarezgarcia@outlook.com
# -------------------------------------

import streamlit as st
import time
from datetime import datetime, timedelta
from fetch import *
from update import *

st.title("IoT Covid-19 Capacity Regulation System")

# Total Number of People currently Inside

total_people = fetch_total_people()

st.metric("Total Number of People Inside Building", total_people, delta=None, delta_color="normal")

# Change Max Capacity Input

number = st.number_input('Insert a number to change Maximum Capacity: ', step=1)

if st.button('Change Maximum Capacity') and number >= 0:
    update_capacity(int(number))
    st.write('Capacity has been changed succesfully.')
    time.sleep(3)
else:
    pass

# Date & Time Selection

current_date = st.date_input(
     "Select a Date: ",
     datetime.now())

st.write('Selected Date is:', current_date)

time1, time2 = st.columns(2)

with time1:
    t1 = st.time_input('Select Beginning Time for Interval: ', datetime.now() - timedelta(hours=3, minutes=0))
    st.write('Selected Beginning Time is: ', t1)

with time2:
    t2 = st.time_input('Select Ending Time for Interval: ', datetime.now() + timedelta(hours=3, minutes=0))
    st.write('Selected Ending Time is: ', t2)

# Entrance & Exit Frames

entrance_f, exit_f = st.columns(2)

entrance_frame = fetch_entrance(str(current_date),str(t1),str(t2))
exit_frame = fetch_exit(str(current_date),str(t1),str(t2))

with entrance_f:
    if(not entrance_frame.empty): st.table(entrance_frame)

with exit_f:
    if(not exit_frame.empty): st.table(exit_frame)

# ------------------------------
# Re-Run App every half a second
# ------------------------------

time.sleep(0.5)

st.experimental_rerun()