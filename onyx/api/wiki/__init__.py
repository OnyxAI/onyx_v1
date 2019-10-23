# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import wikipedia

from onyx.api.assets import Json
from onyx.util import getLogger
from onyx.api.exceptions import *

logger = getLogger('Wikipedia')
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
        except Exception as e:
            logger.error('Getting wiki article error : ' + str(e))
            raise WikiException(str(e))

    def get_summary(self):
        try:
            wikipedia.set_lang(self.lang)
            summary = wikipedia.summary(self.search)

            return summary
        except:
            logger.error('Getting wiki summary error : ' + str(e))
            raise WikiException(str(e))
