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
from flask import render_template, request , redirect , url_for, flash, g
from flask.ext.login import login_required
from onyx.api.plugins import *
from onyxbabel import gettext
import onyx
import os
from onyx.api.assets import decodeJSON
from onyx.decorators import admin_required

@core.route('plugins')
@login_required
@admin_required
def plugins():
	plugins = [d for d in os.listdir(onyx.__path__[0] + "/plugins/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/plugins/", d))]
	plugins.remove('__pycache__')
	plug = []
	for plugin in plugins:
		data = decodeJSON.package(plugin)
		e = {}
		e['name'] = data['name']
		e['raw'] = data['raw']
		e['desc'] = data['description']
		e['version'] = data['version']
		try:
			e['index'] = data['index']
		except KeyError:
			print('No view for ' + data['name'])
		plug.append(e)
	
	try:
		lists = decodeJSON.decodeURL('http://onyxproject.fr/'+g.lang+'/plugin_json')
	except:
		lists = decodeJSON.decodeURL('http://onyxproject.fr/fr/plugin_json')
	return render_template('plugins/index.html', plugins=plug, lists=lists)



@core.route('plugins/install/<string:name>')
@login_required
@admin_required
def install_plugin(name):
	try:
		install(name,request.args['url'])
		flash(gettext('Plugin Installed !'), 'success')
		return redirect(url_for('core.reboot_plugin'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.plugins'))


@core.route('plugins/install_url', methods=['POST'])
@login_required
@admin_required
def install_url():
	if request.method == 'POST':
		try:
			install(request.form['name'],request.form['url'])
			flash(gettext('Plugin Installed !'), 'success')
			return redirect(url_for('core.reboot_plugin'))
		except:
			flash(gettext('An error has occured !'), 'error')
			return redirect(url_for('core.plugins'))


@core.route('plugins/uninstall/<string:name>')
@login_required
@admin_required
def uninstall_plugin(name):
	try:
		uninstall(name)
		flash(gettext('Plugin Uninstalled !'), 'success')
		return redirect(url_for('core.reboot_plugin'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.plugins'))

@core.route('plugins/update/<string:name>')
@login_required
@admin_required
def update_plugin(name):
	try:
		update(name)
		flash(gettext('Plugin Updated !'), 'success')
		return redirect(url_for('core.reboot_plugin'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.plugins'))

@core.route('plugins/reboot')
@login_required
@admin_required
def reboot_plugin():
	return render_template('plugins/reboot.html')