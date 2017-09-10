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
from onyx.util.log import getLogger
from flask import request, render_template, redirect, url_for, flash
from onyxbabel import gettext
from onyx.api.assets import Json
from onyx.api.exceptions import *
from bs4 import BeautifulSoup
try:
	import urllib.request
except ImportError:
	import urllib

logger = getLogger('Transport')
json = Json()

"""
	Get information of RATP service

	Informations sur les différents services de la RATP
"""
class Ratp:

	def __init__(self):
		self.url = None
		self.line = None
		self.station = None
		self.direction = None

	def get_metro_schedule(self):
		try:
			return 'https://api-ratp.pierre-grimaud.fr/v3/schedules/metros/' + self.line + '/' + self.station + '/' + self.direction
		except Exception as e:
			logger.error('Metro error : ' + str(e))
			raise TransportException(str(e))


	def get_rer_schedule(self):
		try:
			return 'https://api-ratp.pierre-grimaud.fr/v3/schedules/rers/' + self.line + '/' + self.station + '/' + self.direction
		except Exception as e:
			logger.error('Rer error : ' + str(e))
			raise TransportException(str(e))
