# kasa_device_manager.py

import asyncio
import kasa
import json


class KasaDeviceManager:
    def __init__(self):
        print("Initializing Kasa Device Manager")
        
        self.devices = self._discover_devices()
        # self._print_devices()

        print("Finished initializing")


    # Private methods
    def _discover_devices(self, json=False):        
        devices = asyncio.run(kasa.Discover.discover(return_raw=json))
        
        return devices

    def _print_devices(self):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())
            print(f"Device: {smart_device}")
            print("--------------------------")

        print("\n")

    def _turn_off_device(self, device: kasa.SmartDevice):
        print(f"Turning {device.alias} off")

        asyncio.run(device.turn_off())

        return True

    def _turn_on_device(self, device: kasa.SmartDevice):
        print(f"Turning {device.alias} on")

        asyncio.run(device.turn_on())

        return True

    def _toggle_device(self, device: kasa.SmartDevice):
        asyncio.run(device.update())

        if device.is_on:
            return self._turn_off_device(device)
        else:
            return self._turn_on_device(device)


    # Public methods
    def get_all_devices(self):
        minified_devices = []

        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())
            minified_device = {
                "name": smart_device.alias, 
                "ip_address": ip_address, 
                "is_on": smart_device.is_on,
                "_links": {
                    "self": { "href": f"/devices/{smart_device.alias.replace(' ', '%20')}" },
                    "toggle": { "href": f"/devices/{smart_device.alias.replace(' ', '%20')}/toggle" }
                }
            }

            minified_devices.append(minified_device)

        devices = {"_embedded": {"devices": minified_devices}}
        return devices

    def get_device(self, device_name):
        minified_device = None

        # Find the device and return the most current state of it
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())

            if device_name.lower() == smart_device.alias.lower():
                minified_device = {
                    "name": smart_device.alias, 
                    "ip_address": ip_address, 
                    "is_on": smart_device.is_on,
                    "system_info": smart_device.sys_info,
                    "_links": {
                        "self": { "href": f"/devices/{smart_device.alias.replace(' ', '%20')}" },
                        "toggle": { "href": f"/devices/{smart_device.alias.replace(' ', '%20')}/toggle" }
                    }
                }

        return minified_device

    def toggle_device_by_ip(self, ip_address):
        device = kasa.SmartDevice(ip_address)

        return self._toggle_device(device)

    def toggle_device_by_name(self, device_name):
        for ip_address, smart_device in self.devices.items():
            asyncio.run(smart_device.update())

            if device_name.lower() == smart_device.alias.lower():
                return self._toggle_device(smart_device)
        
        return False
