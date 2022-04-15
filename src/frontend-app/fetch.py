# -------------------------------------
# IoT Covid-19 Regulation System
# Front-end App
# 'fetch.py'
# Author: Juan Carlos Juárez
# Contact: jc.juarezgarcia@outlook.com
# -------------------------------------

import sqlite3
import os
from datetime import datetime
import pandas as pd

def fetch_total_people():

    db_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','backend-service/system_log.db'))

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    # Entrance Data

    data_query = "SELECT COUNT(*) FROM entrance"

    cursor.execute(data_query)

    data = cursor.fetchall()

    in_number = 0

    for arg in data:
        for arg2 in arg:
            in_number = int(arg2)

    # Exit Data

    data_query = "SELECT COUNT(*) FROM exit"

    cursor.execute(data_query)

    data = cursor.fetchall()

    out_number = 0

    for arg in data:
        for arg2 in arg:
            out_number = int(arg2)

    res = in_number - out_number

    connection.commit()

    if(res <= 0): return 0

    return res

def fetch_entrance(current_date, beginning_time, ending_time):

    db_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','backend-service/system_log.db'))

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    # Entrance Data

    data_query = "SELECT * FROM entrance"

    cursor.execute(data_query)

    data = cursor.fetchall()

    data_tuple = []

    for _tuple in data:
        date = _tuple[0]
        current_tuple = (datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
        data_tuple.append(current_tuple)

    df = pd.DataFrame(data_tuple, columns =['Date & Time of Entrance'])

    if(df.empty): return df

    filtered_date_df = df[df['Date & Time of Entrance'].dt.strftime('%Y-%m-%d') == str(current_date)]

    filtered_time_df = filtered_date_df.loc[(filtered_date_df['Date & Time of Entrance'].dt.strftime('%H:%M:%S') >= str(beginning_time)) & (filtered_date_df['Date & Time of Entrance'].dt.strftime('%H:%M:%S') < str(ending_time))]

    return filtered_time_df

def fetch_exit(current_date, beginning_time, ending_time):

    db_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','backend-service/system_log.db'))

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    # Entrance Data

    data_query = "SELECT * FROM exit"

    cursor.execute(data_query)

    data = cursor.fetchall()

    data_tuple = []

    for _tuple in data:
        date = _tuple[0]
        current_tuple = (datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
        data_tuple.append(current_tuple)

    df = pd.DataFrame(data_tuple, columns =['Date & Time of Exit'])

    if(df.empty): return df

    filtered_date_df = df[df['Date & Time of Exit'].dt.strftime('%Y-%m-%d') == str(current_date)]

    filtered_time_df = filtered_date_df.loc[(filtered_date_df['Date & Time of Exit'].dt.strftime('%H:%M:%S') >= str(beginning_time)) & (filtered_date_df['Date & Time of Exit'].dt.strftime('%H:%M:%S') < str(ending_time))]

    return filtered_time_df