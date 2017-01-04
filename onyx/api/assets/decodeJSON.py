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
import requests
import json
import onyx

def decodeURL(url) :
	r = requests.get(url, auth=('user', 'pass'))
	t = r.json()
	return t

def decode(jsonToRead) :
	r = jsonToRead
	reply = json.loads(r)
	return reply

def package(folder):
	with open(onyx.__path__[0] + "/plugins/"+folder+"/package.json") as data_file:
		data = json.load(data_file)
	return data

def decode_action(lang):
	try:
		if lang == None:
			with open(onyx.__path__[0] + "/data/sentences/fr.json") as data_file:
				data = json.load(data_file)
			return data
		else:
			with open(onyx.__path__[0] + "/data/sentences/"+lang+".json") as data_file:
				data = json.load(data_file)
			return data
	except:
		return 0

def decode_navbar():
	try:
		with open(onyx.__path__[0] + "/data/user/navbar.json") as data_file:
			data = json.load(data_file)
		return data
	except:
		return 0

def decode_navbar_plugin(folder):
	try:
		with open(onyx.__path__[0] + "/plugins/"+folder+"/navbar.json") as data_file:
			data = json.load(data_file)
		return data
	except:
		return 0
