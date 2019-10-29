#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import sys
import os

from os import path, walk
from flask import json
from flask_script import Manager, Command, Option
from flask_migrate import Migrate, MigrateCommand
from onyx.extensions import db
from onyx.api.server import Server
from onyx.app_config import *
from onyx.util.log import getLogger
from onyx import create_app, AppReloader

from werkzeug.serving import run_simple

app = create_app()

application = AppReloader(create_app)

migrate = Migrate(app, db)
manager = Manager(app, with_default_commands=False)
server = Server()

LOG = getLogger(__name__)

class Run(Command):

    option_list = (
        Option('--host', '-h', dest='host', default="0.0.0.0"),
        Option('--port', '-p', dest='port', default=8080),
        Option('--debug', '-d', dest='debug', default=False, action="store_true"),
        Option('--reload', '-r', dest='reload', default=True, action="store_true")
    )

    def run(self, host='0.0.0.0', port=8080, debug=False, reload=True):
        self.runserver(host, port, debug, reload)

    def runserver(self, host, port, debug, reload):

        print(' _____   __   _  __    __ __    __ ')
        print('/  _  \ |  \ | | \ \  / / \ \  / / ')
        print('| | | | |   \| |  \ \/ /   \ \/ /')
        print('| | | | | |\   |   \  /     }  {')
        print('| |_| | | | \  |   / /     / /\ \ ')
        print('\_____/ |_|  \_|  /_/     /_/  \_\ ')
        print('')
        print('-------------------------------------------------------')
        print('')
        LOG.info('Environment: ' + "Debug" if debug else "Production" )
        LOG.info('Port: ' + str(port))
        print('')
        print('-------------------------------------------------------')
        print('')
        LOG.info('Last Version: ' + server.get_last_version())
        LOG.info('Current Version: ' + server.get_version())
        print('')
        print('')
        from datetime import datetime
        LOG.info(datetime.utcnow())
        print('')
        print('-------------------------------------------------------')
        LOG.info('You can access to Onyx with : http://'+host+':'+str(port))
        LOG.info('You can close Onyx at any time with Ctrl-C')
        print('')
        print('-------------------------------------------------------')

        """
        extra_dirs = [app.config['SKILL_FOLDER']]
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in walk(extra_dir):
                for filename in files:
                    filename = path.join(dirname, filename)
                    if path.isfile(filename):
                        extra_files.append(filename)
        """


        run_simple(host, int(port), application, use_debugger=debug, use_reloader=reload, threaded=True)


manager.add_command('run', Run())
manager.add_command('db', MigrateCommand)

if __name__=='__main__':
    manager.run()
