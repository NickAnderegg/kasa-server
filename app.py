# app.py

from flask import Flask
from flask import Response
from flask import request
from kasa_device_manager import KasaDeviceManager
import json

app = Flask(__name__)
kasaDeviceManager = KasaDeviceManager()


@app.route('/devices')
def get_all_devices():
    """
    Returns all the Kasa devices found in the home.
    ---
    GET:
      responses:
        200:
            description: Returns a list of devices
            content: application/json
        404:
            description: Returns when no devices are found
            content: application/json
    """

    devices = kasaDeviceManager.get_all_devices()

    if len(devices['_embedded']['devices']) == 0:
        return Response(json.dumps({"error": "no devices found"}), status=404, mimetype='application/json')
    else:
        return Response(json.dumps(devices), status=200, mimetype='application/json')

@app.route('/devices/<string:device_name>')
def get_device(device_name):
    """
    Returns the Kasa device
    ---
    GET:
      responses:
        200:
            description: Returns the device
            content: application/json
        404:
            description: Returns an error when a device with the specified name is not found
            content: application/json
    """

    device = kasaDeviceManager.get_device(device_name)

    if device == None:
        return Response(json.dumps({"error": "no device found"}), status=404, mimetype='application/json')
    else:
        return Response(json.dumps(device), status=200, mimetype='application/json')

@app.route('/devices/<string:device_name>/toggle', methods=['PUT'])
def toggle_device(device_name):   
    """
    Toggle's a Kasa smart device
    http://127.0.0.1:5000/devices/entry%20lamp%20plug/toggle
    ---
    PUT:
      responses:
        204:
            description: Returns a no content response upon success
            content: application/json
        404:
            description: Returns an error when a device with the specified name is not found
            content: application/json
    """ 

    response = kasaDeviceManager.toggle_device_by_name(device_name)

    if not response:
        return Response(json.dumps({"error": "device not found"}), status=404, mimetype='application/json')
    else:
        return Response('', status=204)