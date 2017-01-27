# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
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
import logging

logger = logging.getLogger()
json = Json()
user = User()
navbar = Navbar()


class Server:

    def __init__(self):
        self.app = None
        self.user = None
        self.lang = None
        self.email = None
        self.id = None
        self.admin = None
        self.avatar = None
        self.buttonColor = 'None'

    def get_version(self):
        try:
            import Onyx
            return Onyx.__version__
        except:
            return "0.3.12"

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
        g.lang = self.lang
        g.email = self.email
        g.id = self.id
        g.admin = self.admin
        g.avatar = user.get_avatar()
        g.version = self.get_version()
        g.ram = "width: "+str(self.get_ram())+"%"
        g.uptime = self.get_up_stats()
        g.disk = "width: "+str(self.get_disk())+"%"
        g.gapi = self.app.config.get('GAPI')
        g.gcx = self.app.config.get('GCX')
        g.next = request.endpoint


        try:
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
        json.json = notifs.get()
        g.notifs = json.decode()

        all_notifs = Notification()
        json.json = all_notifs.get_all()
        g.all_notifs = json.decode()

        scenarios = Scenario()
        json.json = scenarios.get_all()
        g.scenarios = json.decode()


      except Exception as e:
        logger.error('Server Error : ' + str(e))

    def get_context(self,babel):

        @self.app.context_processor
        def utility_processor():
            def get_params(url):
                function = getattr(importlib.import_module(self.app.view_functions[url].__module__), self.app.view_functions[url].__name__)
                execute = function()
                json.json = execute
                return json.decode()
            return dict(get_params=get_params)

        @self.app.context_processor
        def utility_processor():
            def get_variable(p,variable):
                v = str(variable.encode('ascii'))
                return p[v]
            return dict(get_variable=get_variable)

    	@self.app.context_processor
    	def ButtonColor():
    		try:
    			buttonColor = current_user.buttonColor
    		except:
    			buttonColor = ""
    		return dict(buttonColor=str(buttonColor))

    	@self.app.context_processor
    	def gravatar():
            def urlPicAvatar(id):
                user.id = id
                return user.get_avatar_id()
            return dict(urlPicAvatar=urlPicAvatar)

    	@self.app.context_processor
    	def inject_user():
    		try:
    			return {'user': g.user}
    		except AttributeError:
    			return {'user': None}

    	@self.app.teardown_request
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


    #Update

    def update(self):
        try:
            pip.main(['install', '--upgrade' , "onyxproject"])
            self.migrate()
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Update error : ' + str(e))
            raise ServerException(str(e))
            return json.encode({"status":"error"})

    def migrate(self):
        try:
            from onyx.flask_config import SQLALCHEMY_DATABASE_URI
            from onyx.flask_config import SQLALCHEMY_MIGRATE_REPO
            from migrate.versioning import api
            v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
            migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
            tmp_module = imp.new_module('old_model')
            old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
            exec(old_model, tmp_module.__dict__)
            script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO,tmp_module.meta, db.metadata)
            open(migration, "wt").write(script)
            api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
            v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
            logger.info('New migration saved as ' + migration)
            logger.info('Current database version: ' + str(v))
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Migrate error : ' + str(e))
            raise ServerException(str(e))
            return json.encode({"status":"error"})
