# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import core
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from onyx.decorators import admin_required
from onyx.api.navbar import *
from onyx.api.options import *
from onyx.api.server import *
from onyx.api.exceptions import *
from onyx.api.install import Install

install = Install()
option = Options()
server = Server()

@core.route('options' , methods=['GET','POST'])
@login_required
def options():
	if request.method == 'GET':
		return render_template('options/index.html')
	elif request.method == 'POST':
		try:
			option.lang = request.form['lang']
			if request.form['color'] == None:
				option.color = current_user.buttonColor
			else:
				option.color = request.form['color']
			option.set_account()
			flash(gettext('Account changed successfully' ), 'success')
			return redirect(url_for('core.options'))
		except OptionsException:
			flash(gettext("You don't enter param"), 'success')
			return redirect(url_for('core.options'))

@core.route('shutdown')
@admin_required
@login_required
def shutdown():
	try:
		server.shutdown()
		return render_template('options/close.html')
	except ServerException:
		flash(gettext('An error has occured !'),'error')
		return redirect(url_for('core.index'))


@core.route('maj')
@admin_required
@login_required
def maj():
	try:
		server.update()
		flash(gettext("Onyx is now upgrade !"),'success')
		return redirect(url_for('core.options'))
	except ServerException:
		flash(gettext("An error has occured !"), 'error')
		return redirect(url_for('core.options'))

@core.route('data/update')
@admin_required
@login_required
def update_data_git():
	try:
		install.update_data()
		flash(gettext('Data Modified'), 'success')
		return redirect(url_for('core.options'))
	except DataException:
		flash(gettext('An errorhas occured'), 'error')
		return redirect(url_for('core.options'))
