#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import sys
reload(sys)
sys.dont_write_bytecode = True
sys.setdefaultencoding('utf-8')

from flask import json
from flask_script import Manager, Command, Option

import os

from onyx import *
from onyx.extensions import db
from onyx.api.server import *
from onyx.flask_config import *
import onyx

app = create_app()

manager = Manager(app, with_default_commands=False)
server = Server()

class Run(Command):

    option_list = (
        Option('--host', '-h', dest='host', default="0.0.0.0"),
        Option('--port', '-p', dest='port', default=8080),
        Option('--debug', '-d', dest='debug', default=False, action="store_true"),
        Option('--reload', '-r', dest='reload', default=False, action="store_true")
    )

    def run(self, host='0.0.0.0', port=8080, debug=False, reload=False):
        self.runserver(host, port, debug, reload)

    def sync_blueprints(self, app):
        blueprints_fabrics(app, get_blueprints(app))
        error_pages(app, get_blueprint_name(app))

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
        logger.info('Environment: ' + "Debug" if debug else "Production" )
        logger.info('Port: '+ str(port))
        print('')
        print('-------------------------------------------------------')
        from datetime import datetime
        logger.info(datetime.utcnow())
        print('')
        version = server.get_version()
        last_version = server.get_last_version()
        if version != None:
            logger.info('Onyx Version : '+version)
            logger.info('Onyx Last Version : '+last_version)
            if version != last_version:
                server.update()
        print('')
        print('-------------------------------------------------------')
        logger.info('You can access to Onyx with : http://'+host+':'+str(port))
        logger.info('You can close Onyx at any time with Ctrl-C')
        print('')
        print('-------------------------------------------------------')
        self.sync_blueprints(app)
        app.run(host, int(port), debug=debug, use_reloader=reload)

manager.add_command('run', Run())

def run():
    Run().run()


if __name__=='__main__':
    Run().run()
