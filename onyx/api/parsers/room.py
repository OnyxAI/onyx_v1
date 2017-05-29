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
from flask import current_app as app
from onyx.api.room import Room
import re

rooms = Room()
json = Json()

class RoomParser(Parser):

    def __init__(self):
        super(RoomParser, self).__init__()
        json.json = rooms.get()
        self.room = json.decode()

    def parse(self):
        self.result = []
        self.remplaced_str = self.text
        for room in self.room:
            regex = r'(?i)' + re.escape(room['name'])
            search = re.search(regex, self.text)
            if search:
                self.result.append(room['id'])
                self.remplaced_str = self.remplaced_str.replace(search.group(), '%ROOM%')
        return json.encode({"status":"success", "remplaced_str":self.remplaced_str, "kwargs":self.result})
