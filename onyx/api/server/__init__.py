# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import pip, imp
from flask import request
from onyxbabel import gettext
from onyx.extensions import db
import json
from flask import g, request
from flask_login import current_user
from onyx.api.user import *
from onyx.core.models import *
import shutil
import json
import platform
import subprocess
import psutil
import os
import socket
import sys
from onyx.api.assets import decodeJSON
from onyx.api.navbar import *
from onyx.api.house import *
from onyx.api.room import *
from onyx.api.machine import *
from onyx.api.devices import *
from onyx.api.scenario import *
import importlib
import json

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
        ram = psutil.virtual_memory()
        return ram.percent

    def get_disk(self):
        disk = psutil.disk_usage('/')
        return disk.percent

    def get_up_stats(self):
        from uptime import uptime
        m, s = divmod(uptime(), 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def get_vars(self):

        g.user = self.user
        g.lang = self.lang
        g.email = self.email
        g.id = self.id
        g.admin = self.admin
        g.avatar = getAvatar()

        g.version = self.get_version()
        g.ram = "width: "+str(self.get_ram())+"%"
        g.uptime = self.get_up_stats()
        g.disk = "width: "+str(self.get_disk())+"%"
        g.gapi = self.app.config.get('GAPI')
        g.gcx = self.app.config.get('GCX')
        data = decodeJSON.decode_action(g.lang)

        try:
            json_raw = []
            for key in data:
                json_raw.append(key['text'])
                g.action = json_raw
        except:
            g.action = None

        navbar = get_nav()
        list = get_list()
        g.navbar = navbar
        g.list = list

        houses = House()
        g.houses = decodeJSON.decode(houses.get())

        rooms = Room()
        g.rooms = decodeJSON.decode(rooms.get())

        machines = Machine()
        g.machines = decodeJSON.decode(machines.get())

        devices = Devices()
        g.devices = decodeJSON.decode(devices.get())

        scenarios = get_scenario()
        g.scenarios = scenarios

    def get_context(self,babel):

        @self.app.context_processor
        def utility_processor():
            def get_params(url):
                function = getattr(importlib.import_module(self.app.view_functions[url].__module__), self.app.view_functions[url].__name__)
                execute = function()
                return json.loads(execute)
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
    			return getAvatarById(id)
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
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error Shutdown')
            return json.dumps({"status":"error"})


    #Update

    def update(self):
        try:
            pip.main(['install', '--upgrade' , "onyxproject"])
            self.migrate()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error Update')
            return json.dumps({"status":"error"})

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
            print('New migration saved as ' + migration)
            print('Current database version: ' + str(v))
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error Update')
            return json.dumps({"status":"error"})
