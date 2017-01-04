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
sys.dont_write_bytecode = True
import Onyx
import os
import pip
from multiprocessing import Process

from .onyx import create_app
from .onyx.extensions import db

def run():
	port = "5000"
	ip = "127.0.0.1"
	debug = False
	argv = sys.argv[1:]
	argv.remove('runserver')
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
	version = get_version()
	print('Onyx Version : '+version)
	print('')
	print('-------------------------------------------------------')
	print('You can access to Onyx with : http://'+ip+':'+port)
	print('You can close Onyx at any time with Ctrl-C')
	app = create_app()
	try:
		app.run(ip , port=int(port) , debug=debug)
	except:
		print('Error with Args')
		sys.exit(2)

def init():
    from onyx.plugins import plugin
    for module in plugin:
        try:
            module.first()
        except:
            name = module.get_name()
            print('No Init for '+name)

def runserver():
	run_flask = Process(target = run)
	run_flask.start()
	init_plugin = Process(target = init)
	init_plugin.start()
