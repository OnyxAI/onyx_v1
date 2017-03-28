# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import aiml
import onyx
import importlib
import os
from onyx.config import get_config
from onyx.client.tts import TTSFactory

import abc
import imp

from os.path import join, dirname, splitext, isdir

config = get_config('onyx')
lang = config.get('Base', 'lang')

tts = TTSFactory.create()

kernel = aiml.Kernel()
kernel.setPredicate('base_dir', onyx.__path__[0])
kernel.setPredicate('lang', lang)
kernel.bootstrap(learnFiles=onyx.__path__[0] + "/skills/str-startup.xml", commands="load aiml b")

BASE_SKILLS = ['default']
PRIMARY_SKILLS = []
BLACKLISTED_SKILLS = []
SKILLS_BASEDIR = dirname(__file__)
THIRD_PARTY_SKILLS_DIR = ["/opt/onyx/third_party", "/opt/onyx/skills"]



MainModule = '__init__'

def load_skill(skill_descriptor):
    try:
        print("ATTEMPTING TO LOAD SKILL: " + skill_descriptor["name"])
        skill_module = imp.load_module(
            skill_descriptor["name"] + MainModule, *skill_descriptor["info"])
        if (hasattr(skill_module, 'create') and
                callable(skill_module.create)):
            skill = skill_module.create()
            #skill.initialize()
            print("Loaded " + skill_descriptor["name"])
            return skill
        else:
            print("Module %s does not appear to be skill" % (skill_descriptor["name"]))
    except:
        print("Failed to load skill: " + skill_descriptor["name"])
        raise


def get_skills(skills_folder):
    print("LOADING SKILLS FROM " + skills_folder)
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


def create_skill_descriptor(skill_folder):
    info = imp.find_module(MainModule, [skill_folder])
    return {"name": os.path.basename(skill_folder), "info": info}


def load_skills(skills_root=SKILLS_BASEDIR):
    print("Checking " + skills_root + " for new skills")
    skill_list = []
    skills = get_skills(skills_root)
    for skill in skills:
        if skill['name'] in PRIMARY_SKILLS:
            skill_list.append(load_skill(skill))

    for skill in skills:
        if (skill['name'] not in PRIMARY_SKILLS and
                skill['name'] not in BLACKLISTED_SKILLS):
            skill_list.append(load_skill(skill))
    return skill_list


class OnyxSkill(object):

    def __init__(self, name):
        self.name = name
        self.lang = lang
        self.text = None
        self.response = None

    def get_response(self):
        self.response = kernel.respond(self.text)
        if self.response == "":
            self.response = "Your language is not available in Onyx"

        skill = kernel.getPredicate('skill')
        function = kernel.getPredicate('function')
        param = kernel.getPredicate('param').split('|')

        if (function != "" and skill != ""):
            loaded_skill = load_skill(create_skill_descriptor(os.path.join(SKILLS_BASEDIR, skill)))
            loaded_function = getattr(loaded_skill, function)
            if param != "":
                try:
                    execute = loaded_function(param)
                except:
                    execute = loaded_function()
            else:
                execute = loaded_function()
            self.response = execute
        kernel.setPredicate('param', "")
        kernel.setPredicate('skill', "")
        kernel.setPredicate('function', "")
        self.return_text()
        self.return_tts()

    def return_text(self):
        print("Response: " + self.response)

    def return_tts(self):
        if self.response == "Your language is not available in Onyx":
            tts.lang = "en-US"
        tts.execute(self.response)
