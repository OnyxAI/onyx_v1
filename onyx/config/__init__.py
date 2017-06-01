# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import configparser
import os
import onyx
import json
import inflection
import re
from genericpath import exists, isfile
from os.path import join, dirname, expanduser


#Config Path
def get_path(name):
	return onyx.config.__path__[0] + "/" + name + '.cfg'

#Config Plugin Path
def get_skill_path(folder, name):
	return onyx.skills.__path__[0] + "/" + folder + '/config/' + name + '.cfg'

#Import all Config
def get_config(name):
	config = configparser.ConfigParser()
	path = get_path(name)
	config.read(path)
	return config

#Import Plugin Config
def get_skill_config(folder, name):
	config = configparser.ConfigParser()
	path = get_plugin_path(config,name)
	config.read(path)
	return config
