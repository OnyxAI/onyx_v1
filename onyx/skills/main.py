# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import json
import os
import subprocess
import sys
import time
from os.path import exists, join
from threading import Timer

from onyx.util.lock import Lock  # Creates PID file for single instance
from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message
from onyx.skills.core import load_skill, create_skill_descriptor, \
    MainModule, SKILLS_DIR
from onyx.util import connected
from onyx.util.log import getLogger

logger = getLogger("Skills")


ws = None
loaded_skills = {}
last_modified_skill = 0
skills_directories = []
skill_reload_thread = None
skills_manager_timer = None


def connect():
    global ws
    ws.run_forever()


def _skills_manager_dispatch():
    ws.emit(Message("skill_manager", {}))


def _load_skills():
    global ws, loaded_skills, last_modified_skill, skills_directories, \
        skill_reload_thread

    check_connection()

    # Create a thread that monitors the loaded skills, looking for updates
    skill_reload_thread = Timer(0, _watch_skills)
    skill_reload_thread.daemon = True
    skill_reload_thread.start()


def check_connection():
    if connected():
        ws.emit(Message('onyx.internet.connected'))
    else:
        thread = Timer(1, check_connection)
        thread.daemon = True
        thread.start()


def _get_last_modified_date(path):
    last_date = 0
    # getting all recursive paths
    for root, _, _ in os.walk(path):
        f = root.replace(path, "")
        # checking if is a hidden path
        if not f.startswith(".") and not f.startswith("/."):
            last_date = max(last_date, os.path.getmtime(path + f))

    return last_date


def _watch_skills():
    global ws, loaded_skills, last_modified_skill, \
        id_counter

    # Scan the file folder that contains Skills.  If a Skill is updated,
    # unload the existing version from memory and reload from the disk.
    while True:
        if exists(SKILLS_DIR):
            # checking skills dir and getting all skills there
            list = filter(lambda x: os.path.isdir(
                os.path.join(SKILLS_DIR, x)), os.listdir(SKILLS_DIR))

            for skill_folder in list:
                if skill_folder not in loaded_skills:
                    loaded_skills[skill_folder] = {}
                skill = loaded_skills.get(skill_folder)
                skill["path"] = os.path.join(SKILLS_DIR, skill_folder)
                # checking if is a skill
                if not MainModule + ".py" in os.listdir(skill["path"]):
                    continue
                # getting the newest modified date of skill
                skill["last_modified"] = _get_last_modified_date(skill["path"])
                modified = skill.get("last_modified", 0)
                # checking if skill is loaded and wasn't modified
                if skill.get(
                        "loaded") and modified <= last_modified_skill:
                    continue
                # checking if skill was modified
                elif skill.get(
                        "instance") and modified > last_modified_skill:
                    # checking if skill should be reloaded
                    if not skill["instance"].reload_skill:
                        continue
                    logger.debug("Reloading Skill: " + skill_folder)
                    # removing listeners and stopping threads
                    skill["instance"].shutdown()
                    del skill["instance"]
                skill["loaded"] = True
                skill["instance"] = load_skill(
                    create_skill_descriptor(skill["path"]), ws)
        # get the last modified skill
        modified_dates = map(lambda x: x.get("last_modified"), loaded_skills.values())                           

        if len(list(modified_dates)) > 0:
            last_modified_skill = max(modified_dates)

        # Pause briefly before beginning next scan
        time.sleep(2)


def main():
    global ws
    #lock = Lock('skills')  # prevent multiple instances of this service

    # Connect this Skill management process to the websocket
    ws = WebsocketClient()

    # Listen for messages and echo them for logging
    def _echo(message):
        try:
            _message = json.loads(message)

            message = json.dumps(_message)
        except:
            pass
        logger.debug(message)

    ws.on('message', _echo)

    # Kick off loading of skills
    ws.once('open', _load_skills)
    ws.run_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        skills_manager_timer.cancel()
        for skill in loaded_skills:
            skill.shutdown()
        if skill_reload_thread:
            skill_reload_thread.cancel()

    finally:
        sys.exit()
