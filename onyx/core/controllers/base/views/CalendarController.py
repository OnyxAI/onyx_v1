# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import request, render_template, redirect, url_for
from flask.ext.login import login_required
from .. import core
import json
from onyx.api.calendar import *

events = Calendar()

@core.route('calendar', methods=['GET','POST','PUT'])
@login_required
def calendars():
	if request.method == 'GET':
		events_list = json.loads(events.get())
		return render_template('calendar/index.html', events=events_list)

	elif request.method == 'POST':
		events.title = request.form['title']
		events.notes = request.form['notes']
		events.lieu = request.form['lieu']
		events.color = request.form['color']
		events.startdate = request.form['start']
		events.enddate = request.form['end']
		events.add()
		return redirect(url_for('core.calendars'))

	elif request.method == 'PUT':
		events.id = request.form['id']
		events.startdate = request.form['start']
		events.enddate = request.form['end']
		events.update_date()
		return redirect(url_for('core.calendars'))


@core.route('calendar/<int:id>', methods=['GET','POST'])
@login_required
def calendar(id):
	if request.method == 'POST':
		checked = 'delete' in request.form
		if checked == True:
			events.id = request.form['id']
			events.delete()

		events.id = request.form['id']
		events.title = request.form['title']
		events.notes = request.form['notes']
		events.lieu = request.form['lieu']
		events.color = request.form['color']

		events.update_event()
		return redirect(url_for('core.calendars'))

@core.context_processor
def utility_processor():
    def split(str):
        return str.split(" ")
    return dict(split=split)
