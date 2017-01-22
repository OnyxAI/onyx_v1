# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.geolocalisation import Geolocalisation
from onyx.api.exceptions import *
from onyx.api.assets import Json
from onyxbabel import gettext
import logging

json = Json()
logger = logging.getLogger()
geoloc = Geolocalisation()


class Weather:

    def __init__(self):
        self.latitude = geoloc.get_latitude()
        self.longitude = geoloc.get_longitude()

    def get_str(self):
        try:
            json.url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(self.latitude) + "&lon=" + str(self.longitude) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69"
            result = json.decode_url()
            return gettext('It is ') + str(round(result["list"][0]["temp"]["day"])) + gettext(" ° in ") + str(result["city"]["name"]) + " !"
        except Exception as e:
            logger.error('Getting weather error : ' + str(e))
            raise WeatherException(str(e))

    def get_temp_str(self):
        try:
            json.url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(self.latitude) + "&lon=" + str(self.longitude) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69"
            result = json.decode_url()
            return str(round(result["list"][0]["temp"]["day"])) + "°"
        except Exception as e:
            logger.error('Getting weather error : ' + str(e))
            raise WeatherException(str(e))

    def get_img(self):
        try:
            json.url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(self.latitude) + "&lon=" + str(self.longitude) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69"
            result = json.decode_url()
            if result["list"][0]["weather"][0]["main"] == 'Rain':
                url = "rain.png"
            elif result["list"][0]["weather"][0]["main"] == 'Clear':
                url = "clear.png"
            elif result["list"][0]["weather"][0]["main"] == 'Thunderstorm':
                url = "pikacloud.png"
            elif result["list"][0]["weather"][0]["main"] == 'Drizzle':
                url = "rain.png"
            elif result["list"][0]["weather"][0]["main"] == 'Snow':
                url = "snowing.png"
            elif result["list"][0]["weather"][0]["main"] == 'Atmosphere':
                url = "cloud1.png"
            elif result["list"][0]["weather"][0]["main"] == 'Clouds':
                url = "cloud.png"
            elif result["list"][0]["weather"][0]["main"] == 'Extreme':
                url = "windy.png"
            else:
                url = ""
            return url
        except Exception as e:
            logger.error('Getting weather error : ' + str(e))
            raise WeatherException(str(e))
