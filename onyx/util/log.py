# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import logging

FORMAT = '%(levelname)s - %(message)s - %(name)s - %(asctime)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger("ONYX")
logger.setLevel(logging.DEBUG)

logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('flask_login').setLevel(logging.ERROR)

def getLogger(name="ONYX"):
    return logging.getLogger(name)
