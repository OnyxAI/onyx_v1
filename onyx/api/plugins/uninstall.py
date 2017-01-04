# -*- coding: utf-8 -*-
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
from onyx.api.assets import decodeJSON
from onyx.api.navbar import *

def uninstall(name):
	data = decodeJSON.package(name)
	if data['navbar'] == 'True':
		delete_plugin_navbar(name)
	plugin = importlib.import_module('onyx.plugins.'+name)
	plugin.uninstall()
	shutil.rmtree(onyx.__path__[0] + "/plugins/" + name)
	print('Done')
