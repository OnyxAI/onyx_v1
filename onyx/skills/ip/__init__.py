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

class IPSkill(OnyxSkill):

    def __init__(self):
        super(IPSkill, self).__init__(name="IPSkill")

    def give_ip(self):
        return "192.168.0.29"

    def give_name(self, param):
        return "Hello " + param[0]

def create():
    return IPSkill()
