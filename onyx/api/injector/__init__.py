# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.assets import Json

json = Json()

class Injector:

    def __init__(self):
        self.text = None
        self.remplaced_str = None
        self.result = []
        self.scope = None

    def inject(self):
        self.remplaced_str = self.text
        if self.scope != None:
            for prop in self.scope:
                for fetch in prop.keys():
                    self.remplaced_str = self.remplaced_str.replace(fetch, prop[fetch], 1)

        return json.encode({"status":"success", "remplaced_str":self.remplaced_str})
