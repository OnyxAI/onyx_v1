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
from flask import render_template, request, redirect, url_for, flash
from onyxbabel import gettext
from flask_login import login_required, current_user
from onyx.api.scenario import Scenario
from onyx.api.events import Event
from onyx.api.action import Action
from onyx.api.assets import Json

json = Json()
launcher = Scenario()
events = Event()
actions = Action()

@core.route('scenario')
@login_required
def scenario():
	try:
		events_decoded = json.decode(events.get())
		actions_decoded = json.decode(actions.get())

		return render_template('scenario/index.html', events=events_decoded, actions=actions_decoded)
	except Exception as e:
		print(str(e))
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.index'))

@core.route('scenario',methods=['POST'])
@login_required
def add_scenario():
	try:
		_list = request.form.getlist(request.form.get('event_code') + '_param')

		template = " && ".join(_list)

		launcher.template = template
		launcher.name = request.form.get('scenario')
		launcher.user = current_user.id
		launcher.event = request.form.get('event_code')
		launcher.action = request.form.get(request.form.get('action'))
		launcher.action_param = json.encode(request.form.getlist(request.form.get('action') + '_param'))

		launcher.add()

		flash(gettext('Scenario added successfully !'), 'success')
		return redirect(url_for('core.scenario'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.scenario'))

@core.route('scenario/delete/<int:id>')
@login_required
def delete_scenario(id):
	try:
		launcher.id = id
		launcher.delete()
		
		flash(gettext('Scenario deleted successfully !'),'success')
		return redirect(url_for('core.scenario'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.scenario'))
