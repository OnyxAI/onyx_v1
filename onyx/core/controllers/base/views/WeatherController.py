# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import core
from flask import render_template, request, redirect, url_for, flash
from onyxbabel import gettext
from onyx.api.weather import *
from onyx.api.assets import Json
from flask_login import login_required

weather_api = Weather()
json = Json()

@core.route('weather', methods=['GET', 'POST'])
@login_required
def weather():
    if request.method == 'GET':
        return render_template('weather/index.html')
    elif request.method == 'POST':
        try:
            weather_api.latitude = request.form['latitude']
            weather_api.longitude = request.form['longitude']

            result = weather_api.get_temp_str()
            img = weather_api.get_img()

            return render_template('weather/index.html', result=result, img=img)
        except:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for('core.weather'))

