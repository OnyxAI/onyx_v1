"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import git
from git import Repo
import onyx
import pip
import os

def get_data():
	Repo.clone_from('https://github.com/OnyxProject/Onyx-Data', onyx.__path__[0] + "/data/")
	print('Done')

  
def update_data():
	repo = git.cmd.Git(onyx.__path__[0] + "/data/")
	repo.pull()
	print('Done')