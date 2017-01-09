# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.assets import json

json = Json()

class Geolocalisation:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    def get(self):
        json.url = "http://ip-api.com/json"
        data = json.decode_url()
        return json.encode({"latitude":result['lat'],"longitude":result['lon']})

    def get_all(self):
        json.url = "http://ip-api.com/json"
        data = json.decode_url()
        return data

    def get_latitude(self):
        data = self.get()
        json.json = data
        result = json.decode()
        return rasult['latitude']

    def get_longitude(self):
        data = self.get()
        json.json = data
        result = json.decode()
        return rasult['longitude']
