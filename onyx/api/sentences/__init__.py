# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import g, current_app as app
from onyx.api.assets import Json
from onyxbabel import gettext
import importlib

json = Json()

class Sentences:

    def __init__(self):
        self.app = app
        self.id = None
        self.text = None
        self.next = 'core.index'
        self.label = None
        self.url = None
        self.type_event = None

    def get(self):
        try:
            json.lang = g.lang
            json.data_name = "sentences"
            data = json.decode_data()
            e = 0
            while e < len(data):
                if data[e]['text'] == self.text:
                    self.label = data[e]['label']
                    self.url = data[e]['url']
                    self.type_event = data[e]['type']
                    return self.get_event()
                e+=1
            return json.encode({"status":"unknown command","next":self.next})
        except Exception as e:
            raise

    def get_event(self):
        if self.type_event == 'notification':
            function = getattr(importlib.import_module(self.app.view_functions[self.url].__module__), self.app.view_functions[self.url].__name__)
            execute = function()
            return json.encode({"status":"success","type":"notification","text":execute,"next":self.next})
        elif self.type_event == 'exec':
            function = getattr(importlib.import_module(self.app.view_functions[self.url].__module__), self.app.view_functions[self.url].__name__)
            execute = function()
            return json.encode({"status":"success","type":"exec","next":self.next})
