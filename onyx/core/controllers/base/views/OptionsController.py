"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask import request, render_template
from flask.ext.login import login_required
from onyx.decorators import admin_required

from onyx.api.options import *
from onyx.api.server import *



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
	