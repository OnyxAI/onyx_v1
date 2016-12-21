"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .app import create_app


def runserver():


	import Onyx
	import os
	import pip


	from .extensions import db


	#Check Updates
	print("Onyx is starting")
	print(' _____   __   _  __    __ __    __ ')
	print('/  _  \ |  \ | | \ \  / / \ \  / / ')
	print('| | | | |   \| |  \ \/ /   \ \/ /')
	print('| | | | | |\   |   \  /     }  {')
	print('| |_| | | | \  |   / /     / /\ \ ')
	print('\_____/ |_|  \_|  /_/     /_/  \_\ ')
	try:
		os.rename(str(Onyx.__path__[0]) + "/config_example.py" , str(Onyx.__path__[0]) + "/flask_config.py")
		print('Config File Create')
	except:
		print('Config File Already Create')
	print("Check Update")
	pip.main(['install', '--upgrade' , "onyxproject"])
	app = create_app()
	try:
		app.run('0.0.0.0' , port=80 , debug=False)
	except:
		app.run('0.0.0.0' , port=8080 , debug=False)