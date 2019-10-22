# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
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
from onyx.app_config import Config

config = Config()

#Config Path
def get_path(name):
	return config.ONYX_PATH + "/config/" + name + '.cfg'

#Config Plugin Path
def get_skill_path(folder, name):
	return config.SKILL_FOLDER + folder + '/config/' + name + '.cfg'

#Import all Config
def get_config(name):
	config_return = configparser.ConfigParser()
	path = get_path(name)
	config_return.read(path)
	return config_return

#Import Plugin Config
def get_skill_config(folder, name):
	config_return = configparser.ConfigParser()
	path = get_skill_path(folder, name)
	config_return.read(path)
	return config_return
