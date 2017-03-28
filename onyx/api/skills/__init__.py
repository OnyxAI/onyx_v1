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
from onyx.api.assets import Json
from onyx.api.exceptions import *
from flask import g
import importlib
import onyx, pip, os, git, shutil
import logging
from onyx.skills.core import BASE_SKILLS

logger = logging.getLogger()
json = Json()

from onyx.config import get_config
config = get_config('onyx')

class Skill:

    def __init__(self):
        self.name = None
        self.url = None

    def get(self):
        try:
            skills = [d for d in os.listdir(onyx.__path__[0] + "/skills/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/skills/", d))]
            for base in BASE_SKILLS:
                skills.remove(base)
            skill_tab = []
            for skill in skills:
                json.path = onyx.__path__[0] + "/skills/"+skill+"/package.json"
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
                skill_tab.append(e)
            return json.encode(skill_tab)
        except Exception as e:
            raise SkillException(str(e))
            return json.encode({"status":"error"})

    def get_list(self):
        try:
            json.path = onyx.__path__[0] + "/data/skills/" + config.get('Base', 'lang') + ".json"
            data = json.decode_path()

            return json.encode(data)
        except Exception as e:
            raise SkillException(str(e))
            return json.encode({"status":"error"})

    def install(self):
        try:
            Repo.clone_from(self.url, onyx.__path__[0] + "/skills/" + self.name)
            json.path = onyx.__path__[0] + "/skills/"+self.name+"/package.json"
            data = json.decode_path()
            self.install_dep()
            self.install_pip()
            logger.info('Installation done with success')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Installation error : ' + str(e))
            raise SkillException(str(e))
            return json.encode({"status":"error"})

    def update(self):
        try:
            repo = git.cmd.Git(onyx.__path__[0] + "/plugins/" + self.name)
            repo.pull()
            self.install_dep()
            self.install_pip()
            logger.info('Update done with success')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('update error : ' + str(e))
            raise SkillException(str(e))
            return json.encode({"status":"error"})


    def install_dep(self):
        logger.info('Install dependencies for : ' + self.name)
        json.path = onyx.__path__[0] + "/skills/"+self.name+"/package.json"
        data = json.decode_path()
        deps = data["dependencies"]
        os.system('sudo apt-get update --assume-yes')
        for dep in deps:
            os.system('sudo apt-get install --assume-yes '+dep)


    def install_pip(self):
        logger.info('Install pip dependencies for : ' + self.name)
        json.path = onyx.__path__[0] + "/skills/"+self.name+"/package.json"
        data = json.decode_path()
        deps = data["packages"]
        for dep in deps:
            pip.main(['install', dep])

    def uninstall(self):
        try:
            json.path = onyx.__path__[0] + "/skills/"+self.name+"/package.json"
            data = json.decode_path()
            try:
                plugin = importlib.import_module('onyx.skills.'+self.name)
                plugin.uninstall()
            except Exception as e:
                logger.error('Uninstall function : ' + str(e))
                pass
            shutil.rmtree(onyx.__path__[0] + "/skills/" + self.name)
            logger.info('Uninstall done')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Uninstall error : ' + str(e))
            raise SkillException(str(e))
            return json.encode({"status":"error"})
