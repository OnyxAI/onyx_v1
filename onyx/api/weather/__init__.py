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

geoloc = Geolocalisation()


class Weather:

    def __init__():
        self.latitude = geoloc.get_latitude()
        self.longitude = geoloc.get_longitude()

    def get_str(self):
        lat =
        result = decodeJSON.decodeURL("http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + self.latitude + "&lon=" + self.longitude + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69")
        return "Il fait " + str(round(result["list"][0]["temp"]["day"])) + " degré a " + str(result["city"]["name"]) + " !"
