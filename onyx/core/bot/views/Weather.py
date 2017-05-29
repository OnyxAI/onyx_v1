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
from flask_login import current_user
from onyx.api.weather import *
from onyx.api.assets import Json
from .. import bot

weather = Weather()
json = Json()

@bot.route('get_weather')
def get_weather():
    temp = weather.get_temp_str()

    scope = [{"%WEATHER_TEMP%":temp}]

    result =  json.encode({"status":"success", "label":"get_weather", "scope":scope})
    return result

@bot.route('get_weather_city')
def get_weather_city(kwargs):

    weather.latitude = '50'
    weather.longitude = '2'

    temp = weather.get_temp_str()

    scope = [{"%WEATHER_TEMP%":temp, "%WEATHER_CITY%":kwargs[0]}]

    result =  json.encode({"status":"success", "label":"get_weather_city", "scope":scope})
    return result
