# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.api.exceptions import *
from onyxbabel import gettext
from onyx.api.assets import Json
from .. import widgets
from flask import render_template
from onyx.api.weather import *

temp = Weather()
json = Json()

@widgets.route('weather_1')
def weather_1():
    return render_template('widgets/weather_1.html')

@widgets.route('weather_2')
def weather_2():
    temperature = temp.get_temp_str()
    img = temp.get_img()
    return render_template('widgets/weather_2.html', temperature=temperature, img=img)
