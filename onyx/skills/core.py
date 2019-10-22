# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import abc
import sys
import imp
import time
import importlib

import os.path
import re
from onyx.app_config import Config
from os.path import join, dirname, splitext, isdir

from onyx.client.tts import TTSFactory
from onyx.config import get_config
from onyx.filesystem import FileSystemAccess
from onyx.messagebus.message import Message
from onyx.util.log import getLogger
from functools import wraps


BLACKLISTED_SKILLS = []
SKILLS_DIR = Config().SKILL_FOLDER
sys.path.append(SKILLS_DIR)

config = get_config('onyx')
MainModule = '__init__'

tts = TTSFactory.create()

logger = getLogger(__name__)



def load_skill(skill_descriptor, emitter):
    try:
        logger.info("ATTEMPTING TO LOAD SKILL: " + skill_descriptor["name"])
        if skill_descriptor['name'] in BLACKLISTED_SKILLS:
            logger.info("SKILL IS BLACKLISTED " + skill_descriptor["name"])
            return None
        skill_module = imp.load_module(
            skill_descriptor["name"] + MainModule, *skill_descriptor["info"])
        if (hasattr(skill_module, 'create_skill') and
                callable(skill_module.create_skill)):
            # v2 skills framework
            skill = skill_module.create_skill()
            skill.bind(emitter)
            skill.initialize()
            if (hasattr(skill, 'at_run') and callable(skill.at_run)):
                try:
                    skill.at_run()
                except Exception as e:
                    logger.error('Error at_run for ' + Module.name + ' : ' + str(e))
            logger.info("Loaded " + skill_descriptor["name"])
            return skill
        else:
            logger.warn(
                "Module %s does not appear to be skill" % (
                    skill_descriptor["name"]))
    except:
        logger.error(
            "Failed to load skill: " + skill_descriptor["name"], exc_info=True)
    return None


def get_skills(skills_folder):
    logger.info("LOADING SKILLS FROM " + skills_folder)
    skills = []
    possible_skills = os.listdir(skills_folder)
    for i in possible_skills:
        location = join(skills_folder, i)
        if (isdir(location) and
                not MainModule + ".py" in os.listdir(location)):
            for j in os.listdir(location):
                name = join(location, j)
                if (not isdir(name) or
                        not MainModule + ".py" in os.listdir(name)):
                    continue
                skills.append(create_skill_descriptor(name))
        if (not isdir(location) or
                not MainModule + ".py" in os.listdir(location)):
            continue

        skills.append(create_skill_descriptor(location))
    skills = sorted(skills, key=lambda p: p.get('name'))
    return skills

def get_blueprint(skills_folder):
    all_skill = get_skills(skills_folder)
    skills = []
    for skill in all_skill:
        if skill['name'] != 'None':
            skills.append(imp.load_module(skill["name"] + MainModule, *skill["info"]))
    return skills

def get_skill_function(skills_folder, name):
    all_skill = get_skills(skills_folder)
    for skill in all_skill:
        if skill['name'] == name:
            return imp.load_module(skill["name"] + MainModule, *skill["info"])


def get_raw_name(skills_folder):
    all_skill = get_skills(skills_folder)
    skills = []
    for skill in all_skill:
        if skill['name'] != 'None':
            skills.append(skill["name"])
    return skills


def create_skill_descriptor(skill_folder):
    info = imp.find_module(MainModule, [skill_folder])
    return {"name": os.path.basename(skill_folder), "info": info}


def load_skills(emitter, skills_root=SKILLS_DIR):
    logger.info("Checking " + skills_root + " for new skills")
    skill_list = []
    for skill in get_skills(skills_root):
        skill_list.append(load_skill(skill, emitter))

    return skill_list

def unload_skills(skills):
    for s in skills:
        s.shutdown()


class OnyxSkill(object):
    """
    Abstract base class which provides common behaviour and parameters to all
    Skills implementation.
    """

    def __init__(self, name, emitter=None):
        self.name = name
        self.bind(emitter)
        self.config = config
        self.file_system = FileSystemAccess(join('skills', name))
        self.log = getLogger(name)


    @property
    def lang(self):
        return self.config.get('Base','lang')

    def bind(self, emitter):
        if emitter:
            self.emitter = emitter
            self.__register_stop()

    def __register_stop(self):
        self.stop_time = time.time()
        self.stop_threshold = self.config.get("Skills",'stop_threshold')
        self.emitter.on('onyx.stop', self.__handle_stop)


    def initialize(self):
        """
        Initialization function to be implemented by all Skills.
        """
        raise Exception("Initialize not implemented for skill: " + self.name)

    def speak(self, utterance, lang):
        logger.info("Speak: " + utterance)
        self.emitter.emit(Message("speak", {'utterance': utterance, 'lang': lang}))
        tts.lang = lang
        tts.execute(utterance)

    def finish(self):
        self.emitter.emit(Message("finish"))


    def __handle_stop(self, event):
        self.stop_time = time.time()
        self.stop()

    @abc.abstractmethod
    def stop(self):
        pass

    def is_stop(self):
        passed_time = time.time() - self.stop_time
        return passed_time < self.stop_threshold

    def shutdown(self):
        """
        This method is intended to be called during the skill
        process termination. The skill implementation must
        shutdown all processes and operations in execution.
        """
        self.stop()
