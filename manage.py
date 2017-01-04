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
from flask import json
from flask_script import Manager , Server
from flask_migrate import MigrateCommand
import time
from onyx import create_app
from onyx.extensions import db

from multiprocessing import Process
import sys

manager = Manager(create_app)

def run():
    manager.run()

def init():
    from onyx.plugins import plugin
    for module in plugin:
        try:
            module.first()
        except:
            name = module.get_name()
            print('No Init for '+name)

if __name__=='__main__':
     run_flask = Process(target = run)
     run_flask.start()
     init_plugin = Process(target = init)
     init_plugin.start()
