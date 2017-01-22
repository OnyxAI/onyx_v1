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
from flask import render_template, request , redirect , url_for, flash, g
from flask.ext.login import login_required
from onyx.api.plugins import *
import os
from onyx.api.assets import Json
from onyx.decorators import admin_required
from onyx.api.exceptions import *

json = Json()
plugin = Plugin()

@core.route('plugins')
@login_required
def plugins():
	json.json = plugin.get()
	plug = json.decode()

	json.json = plugin.get_list()
	lists = json.decode()

	return render_template('plugins/index.html', plugins=plug, lists=lists)


@core.route('plugins/install/<string:name>')
@login_required
def install_plugin(name):
	try:
		plugin.name = name
		plugin.url = request.args['url']
		plugin.install()
		flash(gettext('Plugin Installed !'), 'success')
		return redirect(url_for('core.reboot_plugin'))
	except PluginException:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.reboot_plugin'))


@core.route('plugins/install_url', methods=['POST'])
@login_required
def install_url():
	try:
		plugin.name = request.form['name']
		plugin.url = request.form['url']
		plugin.install()
		flash(gettext('Plugin Installed !'), 'success')
		return redirect(url_for('core.reboot_plugin'))
	except PluginException:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.reboot_plugin'))


@core.route('plugins/uninstall/<string:name>')
@login_required
def uninstall_plugin(name):
	try:
		plugin.name = name
		plugin.uninstall()
		flash(gettext('Plugin Uninstalled !'), 'success')
		return redirect(url_for('core.reboot_plugin'))
	except PluginException:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.reboot_plugin'))

@core.route('plugins/update/<string:name>')
@login_required
def update_plugin(name):
	try:
		plugin.name = name
		plugin.update()
		flash(gettext('Plugin Updated !'), 'success')
		return redirect(url_for('core.reboot_plugin'))
	except PluginException:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.reboot_plugin'))

@core.route('plugins/reboot')
@login_required
def reboot_plugin():
	return render_template('plugins/reboot.html')
