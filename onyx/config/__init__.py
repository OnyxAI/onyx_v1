"""
Onyx Project
http://onyx^project.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import configparser
import os 


#Config Path
def get_path(name):
	import onyx.config
	return str(onyx.config.__path__[0]) + "/" + name + '.cfg'

#Config Plugin Path
def get_plugin_path(folder,name):
	import onyx.plugins
	return str(onyx.plugins.__path__[0]) + "/" + folder + '/' + name + '.cfg'

#Import all Config
def get_config(name):
	config = configparser.ConfigParser()
	path = get_path(name)
	config.read(path)
	return config

#Import Plugin Config
def get_plugin_config(folder, name):
	config = configparser.ConfigParser()
	path = get_plugin_path(config,name)
	config.read(path)
	return config