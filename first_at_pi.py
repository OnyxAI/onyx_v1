# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import os
import sys

try:
    import Onyx
    os.system('sudo onyx run -p 80')
except:
    os.system('sudo apt-get update')
    os.system('sudo pip install onyxproject')
    os.system('sudo onyx run -p 80')
