from flask import Flask
from flask import Response
from flask import request
from kasa_device_manager import KasaDeviceManager
import json

app = Flask(__name__)
kasa_device_manager = KasaDeviceManager()


# Endpoints
@app.route('/devices')
def get_all_devices():
    """
    Returns all the Kasa devices found in the home.
    /devices
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

    found_devices = kasa_device_manager.get_all_devices()

    if len(found_devices) == 0:
        return Response(json.dumps({"error": "no devices found"}), status=404, mimetype='application/json')
    else:
        devices = []
        for device, ip_address in found_devices:
            url_formatted_device_name = device.alias.replace(' ', '%20')
            device = {
                "name": device.alias, 
                "ip_address": ip_address, 
                "is_on": device.is_on,
                "_links": {
                    "self": { "href": f"/devices/{url_formatted_device_name}" },
                    "toggle": { "href": f"/devices/{url_formatted_device_name}/toggle" },
                    "on": { "href": f"/devices/{url_formatted_device_name}/on" },
                    "off": { "href": f"/devices/{url_formatted_device_name}/off" }
                }
            }

            devices.append(device)

        devices_hypermedia = {"_links": {"self": {"href": "/devices"}}}
        devices = {"count": len(devices), **devices_hypermedia, "_embedded": {"devices": devices}}

        return Response(json.dumps(devices), status=200, mimetype='application/json')

@app.route('/devices/<string:device_name>')
def get_device(device_name):
    """
    Returns the Kasa device
    /devices/entry%20lamp%20plug
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

    found_device, ip_address = kasa_device_manager.get_device(device_name)

    if found_device == None:
        return Response(json.dumps({"error": "no device found"}), status=404, mimetype='application/json')
    else:
        url_formatted_device_name = found_device.alias.replace(' ', '%20')
        device = {
            "name": found_device.alias, 
            "ip_address": ip_address, 
            "is_on": found_device.is_on,
            "system_info": found_device.sys_info,
            "_links": {
                "self": { "href": f"/devices/{url_formatted_device_name}" },
                "toggle": { "href": f"/devices/{url_formatted_device_name}/toggle" },
                "on": { "href": f"/devices/{url_formatted_device_name}/on" },
                "off": { "href": f"/devices/{url_formatted_device_name}/off" }
            }
        }

        return Response(json.dumps(device), status=200, mimetype='application/json')

@app.route('/devices/<string:device_name>/toggle', methods=['PUT'])
def toggle_device(device_name):   
    """
    Toggle's a Kasa smart device
    devices/entry%20lamp%20plug/toggle
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

    response = kasa_device_manager.toggle_device_by_name(device_name)
    
    return format_device_power_state_response(response)

@app.route('/devices/<string:device_name>/on', methods=['PUT'])
def turn_on_device(device_name):   
    """
    Turns on a Kasa smart device
    /devices/entry%20lamp%20plug/on
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

    response = kasa_device_manager.turn_on_device_by_name(device_name)

    return format_device_power_state_response(response)

@app.route('/devices/<string:device_name>/off', methods=['PUT'])
def turn_off_device(device_name):   
    """
    Turns off a Kasa smart device
    /devices/entry%20lamp%20plug/off
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

    response = kasa_device_manager.turn_off_device_by_name(device_name)
    
    return format_device_power_state_response(response)


# Helper functions
def format_device_power_state_response(response):
    if not response:
        return Response(json.dumps({"error": "device not found"}), status=404, mimetype='application/json')
    else:
        return Response('', status=204)