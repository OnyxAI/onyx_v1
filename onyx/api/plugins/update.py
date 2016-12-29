"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import git
from onyx.api.assets import decodeJSON
import onyx
import pip
import os

def update(name):
	repo = git.cmd.Git(onyx.__path__[0] + "/plugins/" + name)
	repo.pull()
	update_dep(name)
	update_pip(name)
	print('Done')


def update_dep(name):
	print("Install Dependencies")
	data = decodeJSON.package(name)
	deps = data["dependencies"]
	for dep in deps:
		os.system('apt-get install '+dep)


def update_pip(name):
	print("Install Pip Dependencies")
	data = decodeJSON.package(name)
	deps = data["packages"]
	for dep in deps:
		pip.main(['install', dep])