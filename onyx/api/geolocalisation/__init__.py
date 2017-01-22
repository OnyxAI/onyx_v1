# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.assets import Json
from onyx.api.exceptions import *
import logging

logger = logging.getLogger()
json = Json()

class Geolocalisation:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    def get(self):
      try:
        json.url = "http://ip-api.com/json"
        result = json.decode_url()
        return json.encode({"latitude":result['lat'],"longitude":result['lon']})
      except Exception as e:
        logger.error('Get geolocalisation error : ' + str(e))
        raise GeolocException(str(e))

    def get_all(self):
      try:
        json.url = "http://ip-api.com/json"
        data = json.decode_url()
        return data
      except Exception as e:
        logger.error('Get geolocalisation error : ' + str(e))
        raise GeolocException(str(e))

    def get_latitude(self):
      try:
        data = self.get()
        json.json = data
        result = json.decode()
        return result['latitude']
      except Exception as e:
        logger.error('Get geolocalisation error : ' + str(e))
        raise GeolocException(str(e))

    def get_longitude(self):
      try:
        data = self.get()
        json.json = data
        result = json.decode()
        return result['longitude']
      except Exception as e:
        logger.error('Get geolocalisation error : ' + str(e))
        raise GeolocException(str(e))
