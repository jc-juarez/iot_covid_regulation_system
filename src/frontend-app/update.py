# -------------------------------------
# IoT Covid-19 Regulation System
# Front-end App
# 'update.py'
# Author: Juan Carlos Juárez
# Contact: jc.juarezgarcia@outlook.com
# -------------------------------------

import sqlite3
import os
import pandas as pd

def update_capacity(cap):

    db_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','backend-service/system_log.db'))

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    data_query = "UPDATE capacity SET max_capacity = {0} WHERE main_id = 'main'".format(cap)

    cursor.execute(data_query)

    connection.commit()