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
from chatterbot import ChatBot
import time, sys, os, onyx, logging
from onyx.api.exceptions import *
from onyx.app import set_bot

logger = logging.getLogger()
json = Json()

class Bot:

    def __init__(self):
        self.kernel = set_bot()
        self.app = app
        self.id = None
        self.text = None
        self.next = 'core.index'
        self.label = None
        self.param = None
        self.url = None
        self.type_event = None

    def get(self):
        try:
            response = str(self.kernel.get_response(self.text))
            return json.encode({"status":"success","type":"notification","text":response,"next":self.next})
        except Exception as e:
            logger.error('Getting sentence error : ' + str(e))
            raise GetException(str(e))

    def get_event(self):
        try:
            if self.type_event == 'notification':
                function = getattr(importlib.import_module(self.app.view_functions[self.url].__module__), self.app.view_functions[self.url].__name__)
                execute = function()
                return json.encode({"status":"success","type":"notification","text":execute,"next":self.next})
            elif self.type_event == 'exec':
                function = getattr(importlib.import_module(self.app.view_functions[self.url].__module__), self.app.view_functions[self.url].__name__)
                try:
                    execute = function(self.param)
                except:
                    execute = function()
                return json.encode({"status":"success","type":"exec","next":self.next,"text":execute})
        except Exception as e:
            logger.error('Getting Response error : ' + str(e))
            raise SentenceException(str(e))
