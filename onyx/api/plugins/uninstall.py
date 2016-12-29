"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import shutil
import onyx
import importlib

def uninstall(name):
	try:
		shutil.rmtree(onyx.__path__[0] + "/plugins/" + name)
		plugin = importlib.import_module('onyx.plugins.'+name)
		plugin.uninstall()
		print('Done') 
	except:
		print('Error') 