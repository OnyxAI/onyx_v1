# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.parsers import Parser
from onyx.api.assets import Json
import re

json = Json()

class WeatherParser(Parser):

    def __init__(self):
        super(WeatherParser, self).__init__()

    def parse(self):
        self.result = []
        self.remplaced_str = self.text
        regex = r'(?i)' + re.escape("%CITY%")
        search = re.search(regex, self.text)
        if search:
            self.result.append("%CITY%")
            self.remplaced_str = self.remplaced_str.replace(search.group(), '%WEATHER_CITY%')
        return json.encode({"status":"success", "remplaced_str":self.remplaced_str, "kwargs":self.result})
