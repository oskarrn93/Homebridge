import telnetlib, time
from flask import Flask, jsonify, Response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

HOST = "192.168.1.15"
PORT = 8102

MAX_VOLUME = 51
MIN_VOLUME = 0

tn = None

DEBUG = False


def getRealVolume(volume):
    return (volume - 1) / 2

def responseData(tmp1, tmp2):
    response = jsonify({tmp1: tmp2})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def getLocalVolume():
    global tn

    tn.write("?V\r\n")  # Get Volume

    response = tn.expect(["VOL\d{3}\r\n"], 1)

    if DEBUG:
        print response

    if response[0] == 0:
        return int(response[2][3:6])
    else:
        return 0

@app.route('/volume/info')
def getVolume():
    #global tn
    #tn.write("?V\r\n")  # Get Volume
    #response = tn.expect(["VOL\d{3}\r\n"], 1)

    #if DEBUG:
        #print response

    #if response[0] == 0:
        #return responseData("ok",response[2][3:6])
    #else:
        #return responseData("error",response)

    return responseData("ok",getLocalVolume());


@app.route('/power/info')
def getPowerStatus():
    global tn

    tn.write("?P\r\n")  # Get power status

    response = tn.expect(["PWR0\r\n"], 1)

    if DEBUG:
        print response

    if response[0] == 0:
        return responseData("ok","on")
    else:
        return responseData("ok","off")

@app.route('/volume/up')
def volumeUp():
    global tn

    tn.write("VU\r\n")
    return responseData("ok",str(getLocalVolume()))

@app.route('/volume/down')
def volumeDown():
    global tn

    tn.write("VD\r\n")
    return responseData("ok",str(getLocalVolume()))

@app.route('/power/on')
def setPowerOn():
    global tn

    tn.write("PO\r\n")  # Turn on the receiver
    return responseData("ok","on")

@app.route('/power/off')
def setPowerOff():
    global tn

    tn.write("PF\r\n")  # Turn off the receiver
    return responseData("ok","off")

@app.before_first_request
def startup():
    global tn

    tn = telnetlib.Telnet(HOST, PORT)

@app.route('/stop')
def stop():
    global tn

    if tn is not None:
        tn.close()
        tn = None

    return responseData("ok","turned stopped")


@app.route('/status')
def status():
    global tn

    if tn is None:
        return responseData("ok","off")
    else:
        return responseData("ok","on")
