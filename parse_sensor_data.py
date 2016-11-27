import datetime
import json

list_of_sensor_data = []

#class for a sensor object
class Sensor_Data(object):
    temperature_inside = 0
    humidity_inside = 0
    time_inside = ""
    temperature_outside = 0
    time_outside = ""

#create a device object with id and name
def create_Sensor_Data(temperature_inside, humidity_inside, time_inside, temperature_outside, time_outside):
    #sensor_data = Sensor_Data()
    sensor_data = {}
    sensor_data["temperature_inside"] = temperature_inside
    sensor_data["humidity_inside"] = humidity_inside
    sensor_data["time_inside"] = time_inside
    sensor_data["temperature_outside"] = temperature_outside
    sensor_data["time_outside"] = time_outside
    return sensor_data

with open("logged_sensor_data.txt") as f:
    sensor_data = f.readlines()

for sensor_data_entry in sensor_data:
    #print sensor_data_entry
    sensor_data_entry_array = sensor_data_entry.split()

    temperature_inside = sensor_data_entry_array[0]
    humidity_inside = sensor_data_entry_array[1]
    time_inside = sensor_data_entry_array[2] + " " + sensor_data_entry_array[3]

    temperature_outside = sensor_data_entry_array[4]
    time_outside = sensor_data_entry_array[5] + " " + sensor_data_entry_array[6]

    print "\ntemperature_inside: ", temperature_inside
    print "humidity_inside: ", humidity_inside
    print "time_inside: ", time_inside

    print "temperature_outside: ", temperature_outside
    print "time_outside: ", time_outside

    list_of_sensor_data.append(create_Sensor_Data(temperature_inside, humidity_inside, time_inside, temperature_outside, time_outside))

    #print json.dumps(list_of_sensor_data)