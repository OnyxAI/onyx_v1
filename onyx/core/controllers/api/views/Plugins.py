# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import api
from flask import request
from flask.ext.login import login_required
from onyx.api.plugins import *
import os
from onyx.api.assets import Json
from onyx.decorators import admin_required
from onyx.api.exceptions import *

plugin = Plugin()
json = Json

@api.route('plugins')
@login_required
def plugins():
	return plugin.get()

@api.route('plugins/list')
@login_required
def plugins_list():
	return plugin.get_list()


@api.route('plugins/install/<string:name>')
@login_required
def install_plugin(name):
	try:
		plugin.name = name
		plugin.url = request.args['url']
		return plugin.install()
	except PluginException:
		return plugin.install()


@api.route('plugins/install_url', methods=['POST'])
@login_required
def install_url():
	try:
		plugin.name = request.form['name']
		plugin.url = request.form['url']
		return plugin.install()
	except PluginException:
		return plugin.install()


@api.route('plugins/uninstall/<string:name>')
@login_required
def uninstall_plugin(name):
	try:
		plugin.name = name
		plugin.uninstall()
		return plugin.uninstall()
	except PluginException:
		return plugin.uninstall()

@api.route('plugins/update/<string:name>')
@login_required
def update_plugin(name):
	try:
		plugin.name = name
		plugin.update()
		return plugin.update()
	except PluginException:
		plugin.update()
