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

import Onyx
import os
import pip
from multiprocessing import Process
import sys

from .onyx import create_app
from .onyx.extensions import db

def run():
	app = create_app()
	try:
		app.run('0.0.0.0' , port=80 , debug=True)
	except:
		app.run('0.0.0.0' , port=8080 , debug=False)

def init():
    from onyx.plugins import plugin
    for module in plugin:
        try:
            module.first()
        except:
            name = module.get_name()
            print('No Init for '+name)

def runserver():
	#Check Updates
	print("Onyx is starting")
	print(' _____   __   _  __    __ __    __ ')
	print('/  _  \ |  \ | | \ \  / / \ \  / / ')
	print('| | | | |   \| |  \ \/ /   \ \/ /')
	print('| | | | | |\   |   \  /     }  {')
	print('| |_| | | | \  |   / /     / /\ \ ')
	print('\_____/ |_|  \_|  /_/     /_/  \_\ ')
	run_flask = Process(target = run)
	run_flask.start()
	init_plugin = Process(target = init)
	init_plugin.start()

	
