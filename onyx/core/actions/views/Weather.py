# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""


from onyx.api.exceptions import *
from onyxbabel import gettext
from onyx.api.assets import Json
from .. import action
from onyx.api.weather import *

temp = Weather()
json = Json()

@action.route('weather')
def weather():
    return temp.get_str()
