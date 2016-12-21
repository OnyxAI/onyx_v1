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
from onyx.api.assets import decodeJSON
from bs4 import BeautifulSoup
import urllib.request

def setRer(name):
	rer = name
	station = request.form['rerstation']
	direction = request.form['rerdirection']
	try:
		return render_template('transport/ratp/rer/result.html', result=getRerSchedule(rer, station, direction))
	except:
		flash(gettext('An error has occured !') , 'error')
		return redirect(url_for('core.transport'))


def getRerSchedule(line , station , direction) : 
	html = urllib.request.urlopen('http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/' + line + '/' + station + '/' + direction).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result

def getRerURL(url) : 
	html = urllib.request.urlopen(url).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result