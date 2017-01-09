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
import wikipedia

json = Json()

class Wikipedia:

    def __init__(self):
        self.lang = None
        self.search = None

    def get_article(self):
        try:
            wikipedia.set_lang(self.lang)
            article = wikipedia.page(self.search)
            return article
        except:
            raise Exception('Error get Article')
            return json.encode({"status":"error"})

    def get_summary(self):
        try:
            wikipedia.set_lang(self.lang)
            summary = wikipedia.summary(self.search)
            return summary
        except:
            raise Exception('Error get Summary')
            return json.encode({"status":"error"})
