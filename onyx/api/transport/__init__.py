# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import os
import json
from flask import request, render_template, redirect, url_for, flash
from onyxbabel import gettext
from onyx.api.assets import Json
from bs4 import BeautifulSoup
try:
	import urllib.request
except ImportError:
	import urllib

json = Json()

class Ratp:

    def __init__(self):
        self.url = None
        self.line = None
        self.station = None
        self.direction = None

    def get_metro_schedule(self):
        try:
            html = urllib.request.urlopen('http://www.ratp.fr/horaires/fr/ratp/metro/prochains_passages/PP/' + self.station + '/' + self.line + '/' + self.direction).read()
        except:
            html = urllib.urlopen('http://www.ratp.fr/horaires/fr/ratp/metro/prochains_passages/PP/' + self.station + '/' + self.line + '/' + self.direction).read()
        ratp = BeautifulSoup(html)
        result = json.encode({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
    	return result

    def get_rer_schedule(self) :
        try:
            html = urllib.request.urlopen('http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/' + self.line + '/' + self.station + '/' + self.direction).read()
        except:
            html = urllib.urlopen('http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/' + self.line + '/' + self.station + '/' + self.direction).read()
            ratp = BeautifulSoup(html)
        result = json.encode({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
        return result
