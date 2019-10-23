# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import api
from flask import request
from onyx.decorators import api_required
from flask_jwt_extended import get_jwt_identity
from onyx.api.assets import Json
from onyx.api.calendar import Calendar
from onyx.api.exceptions import CalendarException

events = Calendar()
json = Json()

@api.route('calendar', methods=['GET','POST','PUT'])
@api_required
def calendars():
	if request.method == 'GET':
		try:
			current_user = get_jwt_identity()
			events.user = current_user.id

			return events.get()
		except CalendarException as e:
			return json.encode({"status": "error"})

	elif request.method == 'POST':
		try:
			events.user = current_user.id
			events.title = request.form['title']
			events.notes = request.form['notes']
			events.lieu = request.form['lieu']
			events.color = request.form['color']
			events.startdate = request.form['start']
			events.enddate = request.form['end']

			return events.add()
		except CalendarException as e:
			return json.encode({"status": "error"})

	elif request.method == 'PUT':
		try:
			events.user = current_user.id
			events.id = request.form['id']
			events.startdate = request.form['start']
			events.enddate = request.form['end']

			return events.update_date()
		except CalendarException as e:
			return json.encode({"status": "error"})

@api.route('calendar/<int:id>', methods=['GET','POST'])
@api_required
def calendar(id):
	if request.method == 'POST':
		try:
			checked = 'delete' in request.form
			if checked == True:
				events.user = current_user.id
				events.id = request.form['id']
				events.delete()
			events.user = current_user.id
			events.id = request.form['id']
			events.title = request.form['title']
			events.notes = request.form['notes']
			events.lieu = request.form['lieu']
			events.color = request.form['color']

			return events.update_event()
		except CalendarException as e:
			return json.encode({"status": "error"})
