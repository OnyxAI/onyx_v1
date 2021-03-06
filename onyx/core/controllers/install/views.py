# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from . import install
from flask import  render_template, redirect, request, flash, url_for
from flask_login import login_required
from onyxbabel import gettext, refresh
from onyx.extensions import db, login_manager
from onyx.core.models import *
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.api.options import Options
from onyx.config import get_config , get_path
from onyx.api.install import Install
from onyx.api.house import House
from onyx.api.weather import Weather
from onyx.core.models import ConfigModel

options = Options()
installation = Install()
house = House()
weather = Weather()
json = Json()

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))

@install.before_request
def check_install():
    install = ConfigModel.Config.query.filter_by(config='install').first()
    if install == None:
        query = ConfigModel.Config(config='install', value='False')
        db.session.add(query)
        db.session.commit()

        return redirect(url_for('install.index'))
    elif install.value == 'True':
        return redirect(url_for('core.index'))

@install.route('/' , methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('install/index.html')
    elif request.method == 'POST':
        try:
            installation.username = request.form['username']
            installation.password = request.form['password']
            installation.email = request.form['email']

            installation.set()

            house.name = request.form['name']
            house.address = request.form['address']
            house.city = request.form['city']
            house.postal = request.form['postal']
            house.country = request.form['country']
            house.latitude = request.form['latitude']
            house.longitude = request.form['longitude']
            house.add()

            weather.token = request.form['weather_api']
            weather.set_token()

            return redirect(url_for("install.redirect_to_onyx"))
        except Exception as e:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for("install.index"))

@install.route('get_data')
def data():
    try:
        installation.get_data()

        return json.encode({"status": "success"})
    except Exception as e:
        return json.encode({"status": "error"})


@install.route('redirect_to_onyx')
def redirect_to_onyx():
    try:
        install = ConfigModel.Config.query.filter_by(config='install').first()
        install.value = 'True'

        db.session.add(install)
        db.session.commit()

        flash(gettext('Onyx is installed !'), 'success')
        return redirect(url_for('core.index'))
    except:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('install.index'))


@install.route('change_lang', methods=['POST'])
def change_lang():
    try:
        options.lang = request.form.get('lang')
        options.change_lang()

        refresh()

        flash(gettext('The lang was changed ! Please reboot Onyx now') , 'success')
        return redirect(url_for('install.reboot', url='install.index', error_url='install.index'))
    except:
        flash(gettext('An error has occured !') , 'error')
        return redirect(url_for("install.index"))
