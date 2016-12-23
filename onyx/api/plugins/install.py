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
import onyx
import pip
import os

def install(name,url):
	Repo.clone_from(url, onyx.__path__[0] + "/plugins/" + name)
	install_dep(name)
	install_pip(name)
	print('Done')


def install_dep(name):
	print("Install Dependencies")
	data = decodeJSON.package(name)
	deps = data["dependencies"]
	for dep in deps:
		os.system('apt-get install '+dep)


def install_pip(name):
	print("Install Pip Dependencies")
	data = decodeJSON.package(name)
	deps = data["packages"]
	for dep in deps:
		pip.main(['install', dep])