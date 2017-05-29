# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import importlib
import os
import onyx

path = [d for d in os.listdir(onyx.__path__[0] + "/plugins/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/plugins/", d))]


plugin = []
for module in path:
	if module != '__pycache__':
		plugin.append(importlib.import_module('onyx.plugins.'+module))
