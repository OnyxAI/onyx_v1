# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import onyxjokes

from onyx.skills.core import OnyxSkill

class JokesSkill(OnyxSkill):

    def __init__(self):
        super(JokesSkill, self).__init__(name="JokesSkill")

    def get_joke(self):
        return onyxjokes.get_joke(language=self.lang, category='all')


def create():
    return JokesSkill()
