# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
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
from adapt.intent import Intent
from onyx.app_config import Config
from os.path import join, dirname, splitext, isdir

from onyx.client.tts import TTSFactory
from onyx.config import get_config
from onyx.dialog import DialogLoader
from onyx.filesystem import FileSystemAccess
from onyx.messagebus.message import Message
from onyx.util.log import getLogger


BLACKLISTED_SKILLS = []
SKILLS_DIR = Config().SKILL_FOLDER
sys.path.append(SKILLS_DIR)

config = get_config('onyx')
MainModule = '__init__'

tts = TTSFactory.create()

logger = getLogger(__name__)


def load_vocab_from_file(path, vocab_type, emitter):
    if path.endswith('.voc'):
        with open(path, 'r') as voc_file:
            for line in voc_file.readlines():
                parts = line.strip().split("|")
                entity = parts[0]

                emitter.emit(Message("register_vocab", {
                    'start': entity, 'end': vocab_type
                }))
                for alias in parts[1:]:
                    emitter.emit(Message("register_vocab", {
                        'start': alias, 'end': vocab_type, 'alias_of': entity
                    }))


def load_regex_from_file(path, emitter):
    if path.endswith('.rx'):
        with open(path, 'r') as reg_file:
            for line in reg_file.readlines():
                re.compile(line.strip())
                emitter.emit(
                    Message("register_vocab", {'regex': line.strip()}))


def load_vocabulary(basedir, emitter):
    for vocab_type in os.listdir(basedir):
        if vocab_type.endswith(".voc"):
            load_vocab_from_file(
                join(basedir, vocab_type), splitext(vocab_type)[0], emitter)


def load_regex(basedir, emitter):
    for regex_type in os.listdir(basedir):
        if regex_type.endswith(".rx"):
            load_regex_from_file(
                join(basedir, regex_type), emitter)


def open_intent_envelope(message):
    intent_dict = message.data
    return Intent(intent_dict.get('name'),
                  intent_dict.get('requires'),
                  intent_dict.get('at_least_one'),
                  intent_dict.get('optional'))


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
            skill.load_data_files(dirname(skill_descriptor['info'][1]))
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
        self.dialog_renderer = None
        self.file_system = FileSystemAccess(join('skills', name))
        self.registered_intents = []
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

    def detach(self):
        for name in self.registered_intents:
            self.emitter.emit(Message("detach_intent", {"intent_name": name}))

    def initialize(self):
        """
        Initialization function to be implemented by all Skills.

        Usually used to create intents rules and register them.
        """
        raise Exception("Initialize not implemented for skill: " + self.name)

    def register_intent(self, intent_parser, handler):
        self.emitter.emit(Message("register_intent", intent_parser.__dict__))
        self.registered_intents.append(intent_parser.name)

        def receive_handler(message):
            try:
                handler(message)
            except:
                # TODO: Localize
                self.speak(
                    "An error occurred while processing a request in " +
                    self.name)
                logger.error(
                    "An error occurred while processing a request in " +
                    self.name, exc_info=True)

        self.emitter.on(intent_parser.name, receive_handler)

    def disable_intent(self, intent_name):
        """Disable a registered intent"""
        logger.debug('Disabling intent ' + intent_name)
        name = self.name + ':' + intent_name
        self.emitter.emit(Message("detach_intent", {"intent_name": name}))

    def enable_intent(self, intent_name):
        """Reenable a registered intent"""
        for (name, intent) in self.registered_intents:
            if name == intent_name:
                self.registered_intents.remove((name, intent))
                intent.name = name
                self.register_intent(intent, None)
                logger.debug('Enabling intent ' + intent_name)
                break
            else:
                logger.error('Could not enable ' + intent_name +
                             ', it hasn\'t been registered.')

    def register_vocabulary(self, entity, entity_type):
        self.emitter.emit(Message('register_vocab', {
            'start': entity, 'end': entity_type
        }))

    def register_regex(self, regex_str):
        re.compile(regex_str)  # validate regex
        self.emitter.emit(Message('register_vocab', {'regex': regex_str}))

    def speak(self, utterance):
        #self.emitter.emit(Message("speak", {'utterance': utterance}))
        logger.info("Speak: " + utterance)
        tts.execute(utterance)

    def speak_dialog(self, key, data={}):
        self.speak(self.dialog_renderer.render(key, data))

    def init_dialog(self, root_directory):
        dialog_dir = join(root_directory, 'dialog', self.lang)
        if os.path.exists(dialog_dir):
            self.dialog_renderer = DialogLoader().load(dialog_dir)
        else:
            logger.error('No dialog loaded, ' + dialog_dir + ' does not exist')

    def load_data_files(self, root_directory):
        self.init_dialog(root_directory)
        self.load_vocab_files(join(root_directory, 'vocab', self.lang))
        regex_path = join(root_directory, 'regex', self.lang)
        if os.path.exists(regex_path):
            self.load_regex_files(regex_path)

    def load_vocab_files(self, vocab_dir):
        if os.path.exists(vocab_dir):
            load_vocabulary(vocab_dir, self.emitter)
        else:
            logger.error('No vocab loaded, ' + vocab_dir + ' does not exist')

    def load_regex_files(self, regex_dir):
        load_regex(regex_dir, self.emitter)

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
