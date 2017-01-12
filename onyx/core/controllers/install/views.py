# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import Blueprint, render_template, redirect, request, current_app, g, flash, url_for
from flask.ext.login import login_required
from onyx.extensions import db, login_manager
from onyx.core.models import *
from onyx.api.exceptions import *
from onyx.config import get_config , get_path
from onyx.api.install import Install

installation = Install()
install = Blueprint('install', __name__, url_prefix='/', template_folder='templates')

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))

@install.route('/' , methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('install/index.html')
	elif request.method == 'POST':
        try:
            installation.get_data()
            installation.username = request.form['username']
            installation.password = request.form['password']
            installation.email = request.form['email']
            installation.set()
            flash('Onyx is installed !' , 'success')
            return redirect(url_for("install.finish"))
        except (InstallException, DataException):
            redirect(url_for("install.index"))


@install.route('finish')
@login_required
def finish():
	configPath = get_path('install')
	installConfig = get_config('install')
	installConfig['Install']['install'] = 'True'
	with open(configPath, 'w') as configfile:
		installConfig.write(configfile)
	return render_template('install/finish.html')
