# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import Blueprint
import onyx

core = Blueprint('core', __name__, url_prefix='/' , template_folder=onyx.__path__[0] + '/templates')

from .views import *
