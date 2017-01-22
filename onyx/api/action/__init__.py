# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import importlib
from flask import current_app as app, g
from onyx.api.assets import Json
import os, onyx

json = Json()

class Action:

    def __init__(self):
        self.id = None
        self.app = app
        self.url = None
        self.param = None

    def get(self):
        json.lang = g.lang
        json.data_name = "actions"
        data = json.decode_data()

        plugins = [d for d in os.listdir(onyx.__path__[0] + "/plugins/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/plugins/", d))]
        for plugin in plugins:
            try:
                json.path = onyx.__path__[0] + "/plugins/" + plugin + "/data/actions.json"
                data += json.decode_path()
            except:
                print('Error')

        return data

    def start(self):
        function = getattr(importlib.import_module(self.app.view_functions[self.url].__module__), self.app.view_functions[self.url].__name__)
        try:
            execute = function()
        except TypeError:
            execute = function(self.param)
