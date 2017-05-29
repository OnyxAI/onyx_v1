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

import json
import inflection
import re
from genericpath import exists, isfile
from os.path import join, dirname, expanduser


#Config Path
def get_path(name):
	import onyx
	return str(onyx.config.__path__[0]) + "/" + name + '.cfg'

#Config Plugin Path
def get_plugin_path(folder,name):
	import onyx
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

class ConfigurationManager(object):
    """
    Static management utility for accessing the cached configuration.
    This configuration is periodically updated from the remote server
    to keep in sync.
    """

    __config = None
    __listener = None

    @staticmethod
    def instance():
        """
        The cached configuration.
        Returns:
            dict: A dictionary representing the Mycroft configuration
        """
        return ConfigurationManager.get()

    @staticmethod
    def init(ws):
        # Start listening for configuration update events on the messagebus
        ConfigurationManager.__listener = _ConfigurationListener(ws)


    @staticmethod
    def get(locations=None):
        """
        Get cached configuration.
        Returns:
            dict: A dictionary representing the Mycroft configuration
        """
        if not ConfigurationManager.__config:
            ConfigurationManager.load_defaults()

        if locations:
            ConfigurationManager.load_local(locations)

        return ConfigurationManager.__config

    @staticmethod
    def update(config):
        """
        Update cached configuration with the new ``config``.
        """
        if not ConfigurationManager.__config:
            ConfigurationManager.load_defaults()

        if config:
            ConfigurationManager.__config.update(config)



class _ConfigurationListener(object):
    """ Utility to synchronize remote configuration changes locally
    This listens to the messagebus for 'configuration.updated', and
    refreshes the cached configuration when this is encountered.
    """

    def __init__(self, ws):
        super(_ConfigurationListener, self).__init__()
        ws.on("configuration.updated", self.updated)

    @staticmethod
    def updated(message):
        ConfigurationManager.update(message.data)
