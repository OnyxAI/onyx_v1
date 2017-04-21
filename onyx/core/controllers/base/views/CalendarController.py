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
from flask import request, render_template, redirect, url_for, flash
from onyxbabel import gettext
from onyx.api.exceptions import *
from flask.ext.login import login_required, current_user
from onyx.api.assets import Json
from onyx.api.calendar import *

json = Json()
events = Calendar()

@core.route('calendar', methods=['GET','POST','PUT'])
@login_required
def calendars():
	if request.method == 'GET':
		events.user = current_user.id
		json.json = events.get()
		events_list = json.decode()
		return render_template('calendar/index.html', events=events_list)

	elif request.method == 'POST':
		try:
			events.user = current_user.id
			events.title = request.form['title']
			events.notes = request.form['notes']
			events.lieu = request.form['lieu']
			events.color = request.form['color']
			events.startdate = request.form['start']
			events.enddate = request.form['end']
			events.add()
			return redirect(url_for('core.calendars'))
		except CalendarException:
			flash(gettext('An error has occured'),'error')
			return redirect(url_for('core.calendars'))

	elif request.method == 'PUT':
		try:
			events.user = current_user.id
			events.id = request.form['id']
			events.startdate = request.form['start']
			events.enddate = request.form['end']
			events.update_date()
			return redirect(url_for('core.calendars'))
		except CalendarException:
			flash(gettext('An error has occured'),'error')
			return redirect(url_for('core.calendars'))


@core.route('calendar/<int:id>', methods=['GET','POST'])
@login_required
def calendar(id):
	if request.method == 'POST':
		try:
			checked = 'delete' in request.form
			if checked == True:
				events.user = current_user.id
				events.id = request.form['id']
				events.delete()
			else:
				events.user = current_user.id
				events.id = request.form['id']
				events.title = request.form['title']
				events.notes = request.form['notes']
				events.lieu = request.form['lieu']
				events.color = request.form['color']

				events.update_event()
			return redirect(url_for('core.calendars'))
		except CalendarException:
			flash(gettext('An error has occured'),'error')
			return redirect(url_for('core.calendars'))

@core.context_processor
def utility_processor():
    def split(str):
        return str.split(" ")
    return dict(split=split)
