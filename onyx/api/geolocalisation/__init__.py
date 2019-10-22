# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.util.log import getLogger

logger = getLogger('Geolocalisation')
json = Json()

"""
    This class allows you to retrieve the different information on geolocation

    Cette classe permet de récupérer les différentes informations sur la géolocalisation
"""
class Geolocalisation:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    """
        This function gets latitude and longitude

        Cette fonction récupère la latitude et la longitude
    """
    def get(self):
        try:
            json.url = "http://ip-api.com/json"
            result = json.decode_url()
            return json.encode({"latitude":result['lat'],"longitude":result['lon'],"status":"success"})
        except Exception as e:
            logger.error('Get geolocalisation error : ' + str(e))
            raise GeolocException(str(e))

    """
        This function gets everything

        Cette fonction récupère tout
    """
    def get_all(self):
        try:
            json.url = "http://ip-api.com/json"
            data = json.decode_url()
            return data
        except Exception as e:
            logger.error('Get geolocalisation error : ' + str(e))
            raise GeolocException(str(e))

    """
        This function gets only latitude

        Cette fonction récupère juste la latitude
    """
    def get_latitude(self):
        try:
            data = self.get()
            json.json = data
            result = json.decode()
            return result['latitude']
        except Exception as e:
            logger.error('Get geolocalisation error : ' + str(e))
            raise GeolocException(str(e))

    """
        This function gets only longitude

        Cette fonction récupère juste la longitude
    """
    def get_longitude(self):
        try:
            data = self.get()
            json.json = data
            result = json.decode()
            return result['longitude']
        except Exception as e:
            logger.error('Get geolocalisation error : ' + str(e))
            raise GeolocException(str(e))
