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
from onyx.api.install import Install

install = Install()
option = Options()
server = Server()

@core.route('options' , methods=['GET','POST'])
@login_required
def options():
	if request.method == 'GET':
		"""
		@api {get} /options Request Options
		@apiName getOptions
		@apiGroup Options
		@apiPermission authenticated

		@apiSuccess (200) {String} hostname Get Hostname of Server
		@apiSuccess (200) {String} platform Get Platform of Server
		@apiSuccess (200) {String} ram Get Ram of Server
		@apiSuccess (200) {String} ip Get IP of Server
		@apiSuccess (200) {String} disk Get Disk Used of Server
		@apiSuccess (200) {String} uptime Get Uptime of Server

		@apiSuccess (200) {String} color Color of User
		@apiSuccess (200) {String} lang Lang of User

		@apiError OptionsNotFound No Options Found

		"""
		return render_template('options/index.html')
	elif request.method == 'POST':
		"""
		@api {post} /options Change Options
		@apiName setAccount
		@apiGroup Options
		@apiPermission authenticated

		@apiParam {String} color Color of User
		@apiParam {String} lang Lang of User

		@apiSuccess (200) redirect Redirect to Option

		@apiError ParamNotFound No Param Found

		"""
		try:
			option.lang = request.form['lang']
			if request.form['color'] == None:
				option.color = current_user.buttonColor
			else:
				option.color = request.form['color']
			option.set_account()
			flash(gettext('Account changed successfully' ), 'success')
			return redirect(url_for('core.options'))
		except Exception:
			flash(gettext("You don't enter param"), 'success')
			return redirect(url_for('core.options'))

@core.route('shutdown')
@admin_required
@login_required
def shutdown():
	"""
	@api {get} /shutdown Shutdown Server
	@apiName shutdown()
	@apiGroup Shutdown
	@apiPermission authenticated
	@apiPermission admin

	@apiSuccess (200) shutdown Close Server

	@apiError NoPermission No Admin
	"""
	try:
		server.shutdown()
		return render_template('options/close.html')
	except Exception:
		flash(gettext('An error has occured !'),'error')
		return redirect(url_for('core.index'))


@core.route('maj')
@admin_required
@login_required
def maj():
	"""
	@api {get} /maj Update Onyx
	@apiName maj()
	@apiGroup Update
	@apiPermission authenticated
	@apiPermission admin

	@apiSuccess (200) update Update Onyx

	@apiError NoPermission No Admin
	@apiError NoPip No Pip Install
	"""
	try:
		server.update()
		flash(gettext("Onyx is now upgrade !"),'success')
		return redirect(url_for('core.options'))
	except Exception:
		flash(gettext("An error has occured !"), 'error')
		return redirect(url_for('core.options'))

@core.route('data/update')
@admin_required
@login_required
def update_data_git():
	install.update_data()
	flash(gettext('Data Modified'), 'success')
	return redirect(url_for('core.options'))
