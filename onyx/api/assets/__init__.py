# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.exceptions import *
import os, requests, json, onyx

class Json:

    def __init__(self):
        self.json = None
        self.url = None
        self.path = None
        self.lang = None
        self.data_name = None

    def decode(self):
        try:
            data = json.loads(self.json)
            return data
        except Exception as e:
            raise JsonException(str(e))

    def encode(self, query):
        try:
            encode = json.dumps(query)
            return encode
        except Exception as e:
            raise JsonException(str(e))

    def decode_url(self):
        try:
            data = requests.get(self.url).json()
            return data
        except Exception as e:
            raise JsonException(str(e))

    def decode_path(self):
        try:
            with open(self.path) as data_file:
                data = json.load(data_file)
                return data
        except Exception as e:
            raise JsonException(str(e))

    def decode_data(self):
        try:
            if self.lang == None:
                with open(onyx.__path__[0] + "/data/" + self.data_name + "/fr.json") as data_file:
                    data = json.load(data_file)
                return data
            else:
                with open(onyx.__path__[0] + "/data/" + self.data_name + "/" + self.lang + ".json") as data_file:
                    data = json.load(data_file)
                return data
        except Exception as e:
            raise JsonException(str(e))
