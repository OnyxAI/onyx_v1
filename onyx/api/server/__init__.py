# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import shutil, platform, psutil, os
from flask import g, request
from flask_login import current_user
from onyx.extensions import db
from onyx.api.user import User
from onyx.core.models import ConfigModel
from onyx.api.assets import Json
from onyx.api.navbar import Navbar
from onyx.api.house import House
from onyx.api.room import Room
from onyx.api.token import Token
from onyx.api.machine import Machine
from onyx.api.scenario import Scenario
from onyx.api.notification import Notification
from onyx.api.events import Event
from onyx.app_config import Config
from onyx.api.exceptions import *
from onyx.config import get_config
from uptime import uptime
import logging
import onyx


config = get_config('onyx')

logger = logging.getLogger("Server")
json = Json()
user = User()
navbar = Navbar()
event = Event()


class Server:
	
	def __init__(self):
		self.id = None
		self.avatar = None
		
	def get_version(self):
		try:
			json.path = os.path.dirname(onyx.__path__[0]) + '/version.json'
			data = json.decode_path()
			
			return data['version']
		except Exception as e:
			logger.error('Server error : ' + str(e))
			return None
			
	def get_last_version(self):
		try:
			json.url = "https://raw.githubusercontent.com/OnyxProject/Onyx/master/version.json"
			data = json.decode_url()
			
			return data['version']
		except Exception as e:
			logger.error('Server error : ' + str(e))
			return None
	
	def get_ram(self):
		try:
			ram = psutil.virtual_memory()
			return ram.percent
		except Exception as e:
			logger.error('Server error : ' + str(e))
			
	def get_disk(self):
		try:
			disk = psutil.disk_usage('/')
			return disk.percent
		except Exception as e:
			logger.error('Server error : ' + str(e))
			
	def get_up_stats(self):
		try:
			m, s = divmod(uptime(), 60)
			h, m = divmod(m, 60)
			return "%d:%02d:%02d" % (h, m, s)
		except Exception as e:
			logger.error('Server error : ' + str(e))
		
	def get_vars(self):
		try:
			g.user = self.user

			try:
				g.color = str(self.user.color)
			except:
				g.color = ""

			g.avatar = user.get_avatar()

			query = ConfigModel.Config.query.filter_by(config='lang').first()
			g.lang = query.value

			g.version = self.get_version()
			g.ram = "width: "+str(self.get_ram())+"%"
			g.uptime = self.get_up_stats()
			g.disk = "width: "+str(self.get_disk())+"%"

			g.next = request.endpoint

			if current_user.background_color == '#0e1b30':
				g.text_color = 'white-text'
				g.panel_color = 'blue-grey darken-1'
			elif current_user.background_color == 'efefef':
				g.text_color = ''
				g.panel_color = 'white'

			try:
				navbar.user = current_user.id 
				g.list = json.decode(navbar.get_list())

				g.navbar = json.decode(navbar.get())
			except NavbarException:
				pass

			houses = House() 
			g.houses = json.decode(houses.get())

			tokens = Token() 
			g.tokens = json.decode(tokens.get())

			rooms = Room()
			g.rooms = json.decode(rooms.get())

			machines = Machine()
			g.machines = json.decode(machines.get())

			notifs = Notification()
			notifs.user = current_user.id
 
			g.notifs = json.decode(notifs.get())

			all_notifs = Notification()
			all_notifs.user = current_user.id
			g.all_notifs = json.decode(all_notifs.get_all())

			scenarios = Scenario()
			scenarios.user = current_user.id
			g.scenarios = json.decode(scenarios.get_all())
		
		except AttributeError:
			pass
		except Exception as e:
			logger.error('Server Error : ' + str(e))

    #Shutdown
	def shutdown(self):
		try:
			func = request.environ.get('werkzeug.server.shutdown')
			if func is None:
				raise RuntimeError('Not running with the Werkzeug Server')
			func()
			logger.info('Shutdown ! Bye !')
			return json.encode({"status":"success"})
		except Exception as e:
			logger.error('Shutdown error : ' + str(e))
			raise ServerException(str(e))


    #Update
	def update(self):
		try:
			event.code = "onyx_updated"
			event.template = ""
			event.new()
			logger.info('Update done !')
			
			return json.encode({"status":"success"})
		except Exception as e:
			logger.error('Reboot error : ' + str(e))
			raise ServerException(str(e))


    #Reboot
	def reboot(self):
		try:
			logger.info('Rebooting ! Bye !')
			return json.encode({"status":"success"})
		except Exception as e:
			logger.error('Reboot error : ' + str(e))
			raise ServerException(str(e))
