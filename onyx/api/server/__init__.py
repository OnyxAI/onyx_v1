# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import pip, imp, shutil, platform, subprocess, psutil, os, socket, sys, importlib
from flask import request
from onyxbabel import gettext
from onyx.extensions import db
from flask import g, request
from flask_login import current_user
from onyx.api.user import User
from onyx.core.models import *
from onyx.api.assets import Json
from onyx.api.navbar import *
from onyx.api.house import *
from onyx.api.room import *
from onyx.api.machine import *
from onyx.api.scenario import *
from onyx.api.notification import *
from onyx.api.exceptions import *
from onyx.app_config import Config
import logging
import onyx

from onyx.config import get_config
config = get_config('onyx')

logger = logging.getLogger()
json = Json()
user = User()
navbar = Navbar()


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
        from uptime import uptime
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
            json.json = navbar.get_list()
            g.list = json.decode()

            json.json = navbar.get()
            g.navbar = json.decode()
        except NavbarException:
            pass

        houses = House()
        json.json = houses.get()
        g.houses = json.decode()

        rooms = Room()
        json.json = rooms.get()
        g.rooms = json.decode()

        machines = Machine()
        json.json = machines.get()
        g.machines = json.decode()

        notifs = Notification()
        notifs.user = current_user.id
        json.json = notifs.get()
        g.notifs = json.decode()

        all_notifs = Notification()
        all_notifs.user = current_user.id
        json.json = all_notifs.get_all()
        g.all_notifs = json.decode()

        scenarios = Scenario()
        json.json = scenarios.get_all()
        g.scenarios = json.decode()

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
            return json.encode({"status":"error"})
