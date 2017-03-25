# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.skills.core import OnyxSkill

class MilightSkill(OnyxSkill):

    def __init__(self):
        super(MilightSkill, self).__init__(name="MilightSkill")

def create():
    return MilightSkill()
