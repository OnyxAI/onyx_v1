# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import core
from flask import render_template, request , redirect , url_for, flash, g
from flask_login import login_required
from onyx.api.skills import *
import os
from onyx.api.assets import Json
from onyx.decorators import admin_required
from onyx.api.exceptions import *
from onyxbabel import gettext

json = Json()
skill = Skill()

@core.route('skills')
@login_required
def skills():
	json.json = skill.get()
	skill_list = json.decode()

	json.json = skill.get_list()
	lists = json.decode()

	return render_template('skills/index.html', skills=skill_list, lists=lists)


@core.route('skills/install/<string:name>')
@login_required
def install_skill(name):
	try:
		skill.name = name
		skill.url = request.args['url']
		result = skill.install()
		json.json = result
		decoded = json.decode()
		if decoded['status'] == "success":
			flash(gettext('Skill Installed !'), 'success')
			return redirect(url_for('core.skills'))
		else:
			flash(gettext('An error has occured !'), 'error')
			return redirect(url_for('core.skills'))
	except Exception as e:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.skills'))


@core.route('skills/install_url', methods=['POST'])
@login_required
def install_skill_url():
	try:
		skill.name = request.form['name']
		skill.url = request.form['url']
		result = skill.install()
		json.json = result
		decoded = json.decode()
		if decoded['status'] == "success":
			flash(gettext('Skill Installed !'), 'success')
			return redirect(url_for('core.skills'))
		else:
			flash(gettext('An error has occured !'), 'error')
			return redirect(url_for('core.skills'))
	except Exception as e:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.skills'))


@core.route('skills/uninstall/<string:name>')
@login_required
def uninstall_skill(name):
	try:
		skill.name = name
		result = skill.uninstall()
		json.json = result
		decoded = json.decode()
		if decoded['status'] == "success":
			flash(gettext('Skill Uninstalled !'), 'success')
			return redirect(url_for('core.skills'))
		else:
			flash(gettext('An error has occured !'), 'error')
			return redirect(url_for('core.skills'))
	except Exception as e:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.skills'))

@core.route('skills/update/<string:name>')
@login_required
def update_skill(name):
	try:
		skill.name = name
		skill.update()
		flash(gettext('Skill Updated !'), 'success')
		return redirect(url_for('core.skills'))
	except Exception as e:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.skills'))

@core.route('skills/reboot')
@login_required
def reboot_skill():
	return render_template('skills/reboot.html')
