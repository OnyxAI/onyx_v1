"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import g, request
from flask_login import current_user
from onyx.api.user import *
from onyxbabel import gettext
import shutil
import json
import platform
import subprocess
import psutil
import os
import socket
import sys

def get_ram():
	ram = psutil.virtual_memory()
	return ram.percent

def get_disk():
	disk = psutil.disk_usage('/')
	return disk.percent

def get_up_stats():
	from uptime import uptime
	m, s = divmod(uptime(), 60)
	h, m = divmod(m, 60) 
	return "%d:%02d:%02d" % (h, m, s)

def get_ipaddress():
	return socket.getfqdn()


def getG(app):
	@app.before_request
	def gvar():
		try:
			g.user = current_user.username
			g.lang = current_user.lang
			g.email = current_user.email
			g.id = current_user.id
			g.admin = current_user.admin
			g.avatar = getAvatar()
		except:
			g.user = 'username'
			g.lang = 'fr'
			g.email = 'email'
			g.id = 'id'
			g.admin = 'admin'
			g.avatar = 'avatar'

	@app.before_request
	def gvariables():
		g.version = "0.3.9"
		g.ram = "width: "+str(get_ram())+"%"
		g.uptime = get_up_stats()
		g.disk = "width: "+str(get_disk())+"%"
		g.ip = get_ipaddress()
		g.gapi = app.config.get('GAPI')
		g.gcx = app.config.get('GCX')
		g.action = { gettext('Quel temps fait il ?'): { "id" : "0" , "type" : "url" , "url" : "weather" }, gettext('Weather'): { "id" : "1" , "type" : "url" , "url" : "weather" } }

def getContext(app,babel):

	@app.context_processor
	def ButtonColor():
		try:
			buttonColor = current_user.buttonColor
		except:
			buttonColor = ""
		return dict(buttonColor=str(buttonColor))

	@app.context_processor
	def gravatar():
		def urlPicAvatar(id):
			return getAvatarById(id)
		return dict(urlPicAvatar=urlPicAvatar)


	@app.context_processor
	def getPlat():
		getPlat = platform.system()
		return dict(getPlat=getPlat)

	@app.context_processor
	def getHost():
		getHost = socket.gethostname()
		return dict(getHost=getHost)
  
  
	@app.context_processor
	def inject_user():
		try:
			return {'user': g.user}
		except AttributeError:
			return {'user': None}

	@app.teardown_request
	def teardown_request(exception):
		if exception:
			db.session.rollback()
			db.session.remove()
		db.session.remove()

	@babel.localeselector
	def get_locale():
		if g.lang:
			return g.lang
		return 'fr'