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
from onyx.api.install import data
from onyx.api.house import *



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
		return setAccount()

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
	return shutdown_flask()

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
	return maj_pip()

@core.route('data/update')
@admin_required
@login_required
def update_data_git():
	data.update_data()
	flash(gettext('Data Modified'), 'success')
	return redirect(url_for('core.options'))

@core.route('house/add', methods=['POST'])
@admin_required
@login_required
def add_house():
	try:
		add_house_db()
		flash(gettext('House Add'), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.options'))

@core.route('house/delete/<int:id>')
@admin_required
@login_required
def delete_house(id):
	try:
		delete_house_db(id)
		flash(gettext('House Deleted'), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.options'))


@core.route('room/add', methods=['POST'])
@admin_required
@login_required
def add_room():
	try:
		add_room_db()
		flash(gettext('Room Add'), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.options'))

@core.route('room/delete/<int:id>')
@admin_required
@login_required
def delete_room(id):
	try:
		delete_room_db(id)
		flash(gettext('Room Deleted'), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.options'))

@core.route('machine/add', methods=['POST'])
@admin_required
@login_required
def add_machine():
	try:
		add_machine_db()
		flash(gettext('Machine Add'), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.options'))

@core.route('machine/delete/<int:id>')
@admin_required
@login_required
def delete_machine(id):
	try:
		delete_machine_db(id)
		flash(gettext('Machine Deleted'), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.options'))

@core.route('navbar/update' , methods=['POST'])
@login_required
def update_navbar():
	set_navbar(request.form['last'],request.form['new'])
	flash(gettext('Modified'), 'success')
	return redirect(url_for('core.options'))
