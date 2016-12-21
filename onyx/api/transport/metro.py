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

def setMetro(name):
	line = name
	station = request.form['metrostation']
	direction = request.form['metrodirection']
	try:
		return render_template('transport/ratp/metro/result.html' ,result=getMetroSchedule(line, station, direction))
	except:
		flash(gettext('An error has occured !') , 'error')
		return redirect(url_for('core.transport'))


def getMetroSchedule(line , station , direction) : 
	html = urllib.request.urlopen('http://www.ratp.fr/horaires/fr/ratp/metro/prochains_passages/PP/' + station + '/' + line + '/' + direction).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result

def getMetroURL(url) : 
	html = urllib.request.urlopen(url).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result