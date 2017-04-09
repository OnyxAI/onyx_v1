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

"""
    This class allows to manage all the json

    Cette classe permet de gérer tout le json
"""
class Json:

    def __init__(self):
        self.json = None
        self.name = None
        self.url = None
        self.path = None
        self.lang = None
        self.data_name = None

    """
        This function decodes the json

        Cette fonction décode le json
    """
    def decode(self):
        try:
            data = json.loads(self.json)
            return data
        except Exception as e:
            raise JsonException(str(e))

    """
        This function encodes the json

        Cette fonction encode le json
    """
    def encode(self, query):
        try:
            encode = json.dumps(query)
            return encode
        except Exception as e:
            raise JsonException(str(e))

    """
        This function decodes the json of a url website

        Cette fonction décode le json d'un adresse web
    """
    def decode_url(self):
        try:
            data = requests.get(self.url).json()
            return data
        except Exception as e:
            raise JsonException(str(e))

    """
        This function decodes the package file of a plugin

        Cette fonction décode le fichier package d'un plugin
    """
    def decode_package(self):
        try:
            with open(onyx.__path__[0] + "/plugins/" + self.name + "/package.json") as data_file:
                data = json.load(data_file)
                return data
        except Exception as e:
            raise JsonException(str(e))

    """
        This function decodes the json of a path

        Cette fonction décode le json d'un fichier
    """
    def decode_path(self):
        try:
            with open(self.path) as data_file:
                data = json.load(data_file)
                return data
        except Exception as e:
            raise JsonException(str(e))

    """
        This function decodes the data json of Onyx

        Cette fonction décode le json des données d'Onyx
    """
    def decode_data(self):
        try:
            if self.lang == None:
                with open(onyx.__path__[0] + "/data/" + self.data_name + "/en-US.json") as data_file:
                    data = json.load(data_file)
                return data
            else:
                with open(onyx.__path__[0] + "/data/" + self.data_name + "/" + self.lang + ".json") as data_file:
                    data = json.load(data_file)
                return data
        except Exception as e:
            raise JsonException(str(e))
