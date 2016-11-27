import os
import time
import requests
import json
import datetime
import threading

#######################

logged_sensor_data_file = "/root/Scripts/logged_sensor_data.txt"
threading_timer = None
debug_true_time = 5.0
#debug_false_time = 900.0 #15 minutes
debug_false_time = 360.0 #6 minutes

debug = False
#debug = True

########################


def log_sensor():
    global threading_timer

    r = requests.get("http://192.168.1.5:8080/json/sensor/info?id=135")
    parsed_json = json.loads(r.content)

    temperature_inside = parsed_json["data"][0]["value"]  # temp
    humidity_inside = parsed_json["data"][1]["value"]  # humid
    time_inside = datetime.datetime.fromtimestamp(parsed_json["lastUpdated"])

    r = requests.get("http://192.168.1.5:8080/json/sensor/info?id=136")
    parsed_json = json.loads(r.content)

    temperature_outside = parsed_json["data"][0]["value"]  # temp
    time_outside = datetime.datetime.fromtimestamp(parsed_json["lastUpdated"])

    output = temperature_inside + " " + " " + humidity_inside + " " + str(
        time_inside) + " " + temperature_outside + " " + str(time_outside)

    if debug:
        print output + "\n"

    with open(logged_sensor_data_file, "w") as myfile:
        myfile.write(output + "\n")

    #continue running script
    if debug:
        threading_timer = threading.Timer(debug_true_time, log_sensor)
    else:
        threading_timer = threading.Timer(debug_false_time, log_sensor)

    threading_timer.start()

if __name__ == "__main__":

    print "Log sensor data script started"
    if debug:
        threading_timer = threading.Timer(debug_true_time, log_sensor)
    else:
        threading_timer = threading.Timer(debug_false_time, log_sensor)

    threading_timer.start()
