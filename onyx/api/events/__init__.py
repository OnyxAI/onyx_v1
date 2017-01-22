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
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.action import *
from flask import g
import os, onyx

action = Action()
json = Json()

class Event:

    def init(self):
        self.id = None
        self.code = None

    def get(self):
        try:
            json.lang = g.lang
            json.data_name = "events"
            data = json.decode_data()
        except:
            json.lang = "fr"
            json.data_name = "events"
            data = json.decode_data()

        plugins = [d for d in os.listdir(onyx.__path__[0] + "/plugins/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/plugins/", d))]
        for plugin in plugins:
            try:
                json.path = onyx.__path__[0] + "/plugins/" + plugin + "/data/events.json"
                data += json.decode_path()
            except:
                print('Error')

        return data

    def new(self):
        code = self.code
        query = ScenarioModel.Scenario.query.filter_by(event=code).all()

        for key in query:
            action.url = key.action
            action.param = key.action_param
            action.start()
