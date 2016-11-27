import time, requests, json, math, datetime, flask
from flask import Flask, jsonify

app = Flask(__name__)

# if we use debug mode
DEBUG = False

@app.route('/on/<id>')
def on(id):

    #send_response(id,"turnon")
    r = requests.get("http://192.168.1.5:8080/json/device/turnon?id=" + str(id))
    resp = flask.Response(r.content)
    #resp = flask.Response("on " + id)
    #resp = flask.Response("success")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/off/<id>')
def stop(id):

    #send_response(id,"turnoff")
    r = requests.get("http://192.168.1.5:8080/json/device/turnoff?id=" + str(id))
    resp = flask.Response(r.content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/status/<id>')
def status(id):


    r = requests.get("http://192.168.1.5:8080/json/device/info?id=" + id)
    parsed_json = json.loads(r.content)

    state = parsed_json["state"]

    if state == 1 or state == 16: #on
        resp = flask.Response("1")
    else: #off
        resp = flask.Response("0")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/dim/status/<id>')
def dim_status(id):

    #id = str(id)

    r = requests.get("http://192.168.1.5:8080/json/device/info?id=" + id)
    parsed_json = json.loads(r.content)

    value = parsed_json["statevalue"]

    tmp_value = int(value)
    tmp_value = tmp_value / 2.55
    tmp_value = math.floor(tmp_value)

    tmp_value = int(tmp_value)

    if tmp_value != 0 and tmp_value != 100:
        tmp_value += 1

    value = str(tmp_value)

    print "dim status: ", value

    resp = flask.Response(value)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/dim/set/<id>/<value>')
def dim_set(id,value):

    tmp_value = int(value)

    if tmp_value == 0:
        requests.get("http://192.168.1.5:8080/json/device/turnoff?id=" + id)
    else:
        tmp_value = tmp_value * 2.55
        tmp_value = math.floor(tmp_value)
        tmp_value = int(tmp_value)
        value = str(tmp_value)
        requests.get("http://192.168.1.5:8080/json/device/dim?id=" + id + "&level=" + value)

    #state = state/255 * 100

    resp = flask.Response("dim " + id + " : " + value)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/temperature/<location>')
def temperature(location):
    logged_sensor_data_file = "/root/Scripts/logged_sensor_data.txt"
    list_of_sensor_data = []

    with open(logged_sensor_data_file) as myfile:
        sensor_data = myfile.readlines()

    for sensor_data_entry in sensor_data:
        #print sensor_data_entry
        sensor_data_entry_array = sensor_data_entry.split()

        temperature_inside = sensor_data_entry_array[0]
        humidity_inside = sensor_data_entry_array[1]
        time_inside = sensor_data_entry_array[2] + " " + sensor_data_entry_array[3]

        temperature_outside = sensor_data_entry_array[4]
        time_outside = sensor_data_entry_array[5] + " " + sensor_data_entry_array[6]

    res_temp = "0"
    res_humid = "0"
    if location == "inside":
        res_temp = temperature_inside
        res_humid = humidity_inside
    elif location == "outside":
        res_temp = temperature_outside
        
    jsonobject = "{\"temperature\": " + res_temp + ",\"humidity\": " + res_humid + "}"

    resp = flask.Response(jsonobject)

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/temperature/info')
def temperature_info():
    logged_sensor_data_file = "/root/Scripts/logged_sensor_data.txt"
    list_of_sensor_data = []

    with open(logged_sensor_data_file) as myfile:
        sensor_data = myfile.readlines()

    for sensor_data_entry in sensor_data:
        # print sensor_data_entry
        sensor_data_entry_array = sensor_data_entry.split()

        temperature_inside = sensor_data_entry_array[0]
        humidity_inside = sensor_data_entry_array[1]
        time_inside = sensor_data_entry_array[2] + " " + sensor_data_entry_array[3]

        temperature_outside = sensor_data_entry_array[4]
        time_outside = sensor_data_entry_array[5] + " " + sensor_data_entry_array[6]


        list_of_sensor_data.append(
            create_Sensor_Data(temperature_inside, humidity_inside, time_inside, temperature_outside, time_outside))

    #resp = flask.Response(json.dumps(list_of_sensor_data))
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    #resp.headers['content-type'] = 'application/json'

    resp = flask.Response(response=json.dumps(list_of_sensor_data),status=200, mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

#create a device object with id and name
def create_Sensor_Data(temperature_inside, humidity_inside, time_inside, temperature_outside, time_outside):
    sensor_data = {}
    sensor_data["temperature_inside"] = temperature_inside
    sensor_data["humidity_inside"] = humidity_inside
    sensor_data["time_inside"] = time_inside
    sensor_data["temperature_outside"] = temperature_outside
    sensor_data["time_outside"] = time_outside
    return sensor_data

# send the request to the rest api to either turn on or off the device
# id is the id of the device
# status is either turnon or turnoff
#def send_response(device_id, status):
    #requests.get("http://192.168.1.5:8080/json/device/" + status + "?id=" + str(device_id))
