# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import api
from flask import  request, Response
from onyx.decorators import api_required
from onyx.api.weather import Weather
from onyx.api.assets import Json
from onyx.api.exceptions import *

weather = Weather()
json = Json()

@api.route('weather/daily', methods=['POST'])
@api_required
def weather_daily():
    if request.method == 'POST':
        try:
            weather.latitude = request.form['latitude']
            weather.longitude = request.form['longitude']

            return Response(json.encode(weather.get_daily()), mimetype='application/json')
        except WeatherException:
            return Response(json.encode({"status": "error"}), mimetype='application/json')
