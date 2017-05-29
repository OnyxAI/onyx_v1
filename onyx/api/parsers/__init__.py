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
from flask import current_app as app
from onyx.util.log import getLogger

json = Json()
LOG = getLogger('Parser')

class Parser(object):

    def __init__(self):
        self.app = app
        self.text = None
        self.remplaced_str = None
        self.result = []

    def parse(self):

        from onyx.api.parsers.weather import WeatherParser
        from onyx.api.parsers.room import RoomParser
        from onyx.api.parsers.user import UserParser

        room = RoomParser()
        user = UserParser()
        weather = WeatherParser()

        kwargs = []

        user.text = self.text
        json.json = user.parse()
        user_parsed = json.decode()

        self.remplaced_str = user_parsed['remplaced_str']


        weather.text = self.remplaced_str
        json.json = weather.parse()
        weather_parsed = json.decode()

        self.remplaced_str = weather_parsed['remplaced_str']

        room.text = self.remplaced_str
        json.json = room.parse()
        room_parsed = json.decode()

        self.remplaced_str = room_parsed['remplaced_str']

        kwargs.extend(weather_parsed['kwargs'])
        kwargs.extend(user_parsed['kwargs'])
        kwargs.extend(room_parsed['kwargs'])


        return json.encode({"status":"success", "remplaced_str":self.remplaced_str, "kwargs":kwargs})
