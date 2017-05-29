# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import Blueprint, render_template, redirect, request, current_app as app, g, flash, url_for
from flask.ext.login import login_required
from onyxbabel import gettext
from onyx.extensions import db, login_manager
from onyx.core.models import *
from onyx.api.exceptions import *
from onyx.api.options import *
from onyx.config import get_config , get_path
from onyx.api.install import Install
import onyx, os

options = Options()
installation = Install()
install = Blueprint('install', __name__, url_prefix='/install/', template_folder='templates')

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))

@install.before_request
def check_install():
    if app.config['INSTALL']:
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
            return redirect(url_for("install.redirect_to_onyx"))
        except Exception as e:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for("install.index"))

@install.route('get_data')
def data():
    try:
        installation.get_data()
        return "Get Data successfully"
    except Exception as e:
        return "An error has occured"

@install.route('reboot/<url>/<error_url>')
def reboot(url, error_url):
    try:
        os.system('sudo pm2 restart onyx-client')
        return redirect(url_for(url))
    except:
        flash(gettext('An error has occured !') , 'error')
        return redirect(url_for(error_url))

@install.route('redirect_to_onyx')
def redirect_to_onyx():
    configPath = get_path('onyx')
    installConfig = get_config('onyx')
    installConfig.set('Install', 'done', 'True')
    with open(configPath, 'w') as configfile:
        installConfig.write(configfile)
    flash(gettext('Onyx is installed !'), 'success')
    return redirect(url_for('install.reboot', url='install.finish', error_url='install.finish'))

@install.route('change_lang', methods=['POST'])
def change_lang():
    try:
        options.lang = request.form.get('lang')
        options.change_lang()
        flash(gettext('The lang was changed ! If not please reboot Onyx') , 'success')
        return redirect(url_for('install.reboot', url='install.index', error_url='install.index'))
    except:
        flash(gettext('An error has occured !') , 'error')
        return redirect(url_for("install.index"))

@install.route('finish')
def finish():
    return render_template('install/finish.html')
