# -------------------------------------
# IoT Covid-19 Regulation System
# Back-end Service
# '__main__.py'
# Author: Juan Carlos Juárez
# Contact: jc.juarezgarcia@outlook.com
# -------------------------------------

from flask import Flask
import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# Main Route
@app.route("/")
def entry():
    return "Server is running."

# Entrance Route
@app.route("/backend-api/entrance")
def entrance_log():

    connection = sqlite3.connect(current_dir + "/system_log.db")

    cursor = connection.cursor()

    data_query = "INSERT INTO entrance VALUES(datetime('now', 'localtime'))"

    cursor.execute(data_query)

    connection.commit()

    return "Entrance has been recorded.", 200

# Exit Route
@app.route("/backend-api/exit")
def exit_log():

    connection = sqlite3.connect(current_dir + "/system_log.db")

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

    if((out_number + 1) <= in_number):

        data_query = "INSERT INTO exit VALUES(datetime('now', 'localtime'))"

        cursor.execute(data_query)

        connection.commit()

    return "Exit has been recorded.", 200

# Route for Checking Total Number of People
@app.route("/backend-api/check-total-people")
def check_total_people():

    connection = sqlite3.connect(current_dir + "/system_log.db")

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

    if(res <= 0): return "0", 200

    return str(res), 200

# Route for Checking changed on Max Capacity
@app.route("/backend-api/check-max-capacity")
def update_capacity():

    connection = sqlite3.connect(current_dir + "/system_log.db")

    cursor = connection.cursor()

    data_query = "SELECT * FROM capacity"

    cursor.execute(data_query)

    data = cursor.fetchall()

    current_max_capacity = 0

    # Get the Max Capacity which is the second argument
    current_max_capacity = int(data[0][1])

    current_max_capacity = str(current_max_capacity)

    connection.commit()

    return current_max_capacity, 200

# Route for Updating Temperature
@app.route("/backend-api/set-temperature/<temp>")
def set_temperature(temp):

    connection = sqlite3.connect(current_dir + "/system_log.db")

    cursor = connection.cursor()

    temp = int(temp)

    temp = str(temp)

    data_query = "UPDATE temperature SET current_temperature = {0} WHERE main_id = 'main'".format(temp)

    cursor.execute(data_query)

    connection.commit()

    return "Temperature has been changed."

# Route for Checking Temperature
@app.route("/backend-api/check-temperature")
def check_temperature():

    connection = sqlite3.connect(current_dir + "/system_log.db")

    cursor = connection.cursor()

    data_query = "SELECT * FROM temperature"

    cursor.execute(data_query)

    data = cursor.fetchall()

    current_temp = 0

    # Get the Max Capacity which is the second argument
    current_temp = int(data[0][1])

    current_temp = str(current_temp)

    connection.commit()

    return current_temp, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)