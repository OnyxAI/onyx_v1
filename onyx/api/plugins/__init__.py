# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from git import Repo
from onyx.api.assets import decodeJSON
from onyx.api.navbar import *
import importlib
import onyx
import pip
import os
import json
import git
import shutil

class Plugin:

    def __init__(self):
        self.name = None
        self.url = None

    def get(self):
        try:
            plugins = [d for d in os.listdir(onyx.__path__[0] + "/plugins/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/plugins/", d))]
            plug = []
            for plugin in plugins:
                data = decodeJSON.package(plugin)
                e = {}
                e['name'] = data['name']
                e['raw'] = data['raw']
                e['desc'] = data['description']
                e['version'] = data['version']
                try:
                    e['index'] = data['index']
                except KeyError:
                    print('No view for ' + data['name'])

                    plug.append(e)
            return json.dumps(plug)
        except:
            raise Exception('Error Get')
            return json.dumps({"status":"error"})

    def get_list(self):
        try:
            try:
        		lists = decodeJSON.decodeURL('http://onyxproject.fr/'+g.lang+'/plugin_json')
            except:
                lists = decodeJSON.decodeURL('http://onyxproject.fr/fr/plugin_json')

            return json.dumps(lists)
        except:
            raise Exception('Error Get List')
            return json.dumps({"status":"error"})

    def install(self):
        try:
            Repo.clone_from(self.url, onyx.__path__[0] + "/plugins/" + self.name)
            data = decodeJSON.package(self.name)
            self.install_dep()
            self.install_pip()
            if data['navbar'] == 'True':
                set_plugin_navbar(self.name)
            print('Done Install')
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error Install')
            return json.dumps({"status":"error"})

    def update(self):
        try:
            repo = git.cmd.Git(onyx.__path__[0] + "/plugins/" + self.name)
            repo.pull()
            self.install_dep()
            self.install_pip()
            print('Done Update')
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error Update')
            return json.dumps({"status":"error"})


    def install_dep(self):
    	print("Install Dependencies")
    	data = decodeJSON.package(self.name)
    	deps = data["dependencies"]
    	os.system('apt-get update --assume-yes')
    	for dep in deps:
    		os.system('apt-get install --assume-yes '+dep)


    def install_pip(self):
    	print("Install Pip Dependencies")
    	data = decodeJSON.package(self.name)
    	deps = data["packages"]
    	for dep in deps:
    		pip.main(['install', dep])

    def uninstall(self):
        try:
            data = decodeJSON.package(self.name)
            if data['navbar'] == 'True':
                delete_plugin_navbar(self.name)
            plugin = importlib.import_module('onyx.plugins.'+self.name)
            plugin.uninstall()
            shutil.rmtree(onyx.__path__[0] + "/plugins/" + self.name)
            print('Done Uninstall')
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error Uninstall')
            return json.dumps({"status":"error"})
