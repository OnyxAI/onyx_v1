# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyxbabel import gettext
import time

"""
    Get the time

    Récupèrer l'heure et la date
"""
class Time:

    def __init__(self):
        self.hours = None
        self.minutes = None
        self.seconds = None

    """
        Return a string time

        Retourne une chaine de caractère avec l'heure
    """
    def get(self):
        return time.strftime("%H : %M")
