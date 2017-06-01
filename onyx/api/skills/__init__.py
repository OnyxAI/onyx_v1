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
from flask import g, current_app as app
import importlib
import onyx, pip, os, git, shutil

from onyx.api.widgets import *
from onyx.api.scenario import *
from onyx.api.navbar import *
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.util import getLogger

scenario = Scenario()
widgets = Widgets()
navbar = Navbar()
logger = getLogger(__name__)
json = Json()

from onyx.config import get_config
config = get_config('onyx')

class Skill:

    def __init__(self):
        self.name = None
        self.url = None
        self.config = config
        self.app = app

    def get(self):
        try:
            skills = [d for d in os.listdir(self.app.config['SKILL_FOLDER']) if os.path.isdir(os.path.join(self.app.config['SKILL_FOLDER'], d))]
            try:
                skills.remove('__pycache__')
            except:
                pass
            skill_tab = []
            for skill in skills:
                json.path = self.app.config['SKILL_FOLDER'] +skill+"/package.json"
                data = json.decode_path()
                e = {}
                e['name'] = data['name']
                e['raw'] = data['raw']
                e['desc'] = data['description']
                e['version'] = data['version']
                try:
                    e['index'] = data['index']
                except KeyError:
                    print('No view for ' + data['name'])
                try:
                    e['config'] = data['config']
                except KeyError:
                    print('No config for ' + data['name'])
                skill_tab.append(e)
            return json.encode(skill_tab)
        except Exception as e:
            logger.error("An error has occured : " + str(e))
            return json.encode({"status":"error"})

    def get_list(self):
        try:
            json.path = self.app.config['DATA_FOLDER'] + "/skills/" + self.config.get('Base', 'lang') + ".json"
            data = json.decode_path()

            return json.encode(data)
        except Exception as e:
            logger.error("An error has occured : " + str(e))
            return json.encode({"status":"error"})

    def install(self):
        try:
            Repo.clone_from(self.url, self.app.config['SKILL_FOLDER'] + self.name)
            json.path = self.app.config['SKILL_FOLDER'] + self.name + "/package.json"
            data = json.decode_path()
            self.install_dep(data)
            self.install_pip(data)
            logger.info('Installation done with success')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Installation error : ' + str(e))
            return json.encode({"status":"error"})

    def update(self):
        try:
            repo = git.cmd.Git(self.app.config['SKILL_FOLDER'] + self.name)
            repo.pull()
            json.path = self.app.config['SKILL_FOLDER'] + self.name + "/package.json"
            data = json.decode_path()
            self.install_dep(data)
            self.install_pip(data)
            logger.info('Update done with success')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Update error : ' + str(e))
            return json.encode({"status":"error"})


    def install_dep(self, data):
        try:
            logger.info('Install dependencies for : ' + self.name)
            deps = data["dependencies"]
            for dep in deps:
                os.system('sudo apt-get install --assume-yes '+dep)
        except Exception as e:
            logger.error("An error has occured : " + str(e))



    def install_pip(self, data):
        try:
            logger.info('Install pip dependencies for : ' + self.name)
            deps = data["packages"]
            for dep in deps:
                os.system('pip3 install ' + dep)
        except Exception as e:
            logger.error("An error has occured : " + str(e))


    def uninstall(self):
        try:
            json.path = self.app.config['SKILL_FOLDER'] + self.name + "/package.json"
            data = json.decode_path()
            shutil.rmtree(self.app.config['SKILL_FOLDER'] + self.name)
            logger.info('Uninstall done')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Uninstall error : ' + str(e))
            return json.encode({"status":"error"})
