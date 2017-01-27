"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.dont_write_bytecode = True
sys.setdefaultencoding('utf-8')
from flask import json
from flask_script import Manager
from flask_migrate import MigrateCommand
import time
import os
from onyx import create_app
from onyx.extensions import db
from onyx.api.server import *
from flask._compat import text_type
import onyx
import shutil
manager = Manager(create_app)
import getopt

server = Server()

def run():
    port = "5000"
    ip = "127.0.0.1"
    env = "Production"
    argv = sys.argv[1:]
    argv.remove('runserver')
    try:
        argv.remove('-r')
    except:
        pass
    if '-d' in argv:
        env = "Debug"
    try:
        argv.remove('-d')
    except:
        pass
    myopts, args = getopt.getopt(argv,"h:p:")
    for o, a in myopts:
        if o == '-p':
            port=a
        elif o == '-h':
            ip=a
        else:
            pass
    print(' _____   __   _  __    __ __    __ ')
    print('/  _  \ |  \ | | \ \  / / \ \  / / ')
    print('| | | | |   \| |  \ \/ /   \ \/ /')
    print('| | | | | |\   |   \  /     }  {')
    print('| |_| | | | \  |   / /     / /\ \ ')
    print('\_____/ |_|  \_|  /_/     /_/  \_\ ')
    print('')
    print('-------------------------------------------------------')
    print('')
    print('Environment: ' + env)
    print('Port: '+ port)
    print('')
    print('-------------------------------------------------------')
    from datetime import datetime
    print(datetime.utcnow())
    print('')
    version = server.get_version()
    print('Onyx Version : '+version)
    print('')
    print('-------------------------------------------------------')
    print('You can access to Onyx with : http://'+ip+':'+port)
    print('You can close Onyx at any time with Ctrl-C')
    print('')
    print('-------------------------------------------------------')
    try:
        if os.path.exists(str(onyx.__path__[0]) + "/flask_config.py"):
            print('Config Already File Create')
        else:
            os.rename(str(onyx.__path__[0]) + "/config_example.py" , str(onyx.__path__[0]) + "/flask_config.py")
            print('Config File Create')
    except:
        print('Config Already File Create')
    try:
        if os.path.exists(str(onyx.__path__[0]) + "/data/.gitkeep"):
            shutil.rmtree(str(onyx.__path__[0]) + "/data/.gitkeep")
            print('Data Added')
        else:
            print('Data Already Add')
    except:
        print('Data Already Add')
    manager.run()


if __name__=='__main__':
    run()
