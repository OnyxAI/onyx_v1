# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""


import json
import sys
import time
from threading import Timer

import os
from os.path import expanduser, exists

from onyx.skills.core import load_skills, THIRD_PARTY_SKILLS_DIR, \
    load_skill, create_skill_descriptor, MainModule




def main():
    load_skills()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        for skill in loaded_skills:
            skill.shutdown()
        if skill_reload_thread:
            skill_reload_thread.cancel()

    finally:
        sys.exit()
