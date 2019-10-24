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
from flask import request, Response, session
from onyx.decorators import api_required
from flask_jwt_extended import get_jwt_identity, decode_token
from onyx.api.assets import Json
from onyx.api.calendar import Calendar
from onyx.api.exceptions import CalendarException

events = Calendar()
json = Json()

@api.route('calendar', methods=['GET','POST','PUT'])
@api_required
def calendars():
	try:
		current_user = decode_token(session['token'])['identity']
	except:	
		current_user = get_jwt_identity()
	if request.method == 'GET':
		try:
			events.user = current_user['id']

			return Response(events.get(), mimetype='application/json')
		except CalendarException as e:
			return Response(json.encode({"status": "error"}), mimetype='application/json')

	elif request.method == 'POST':
		try:
			events.user = current_user['id']
			events.title = request.form['title']
			events.notes = request.form['notes']
			events.lieu = request.form['lieu']
			events.color = request.form['color']
			events.startdate = request.form['start']
			events.enddate = request.form['end']

			return Response(events.add(), mimetype='application/json')
		except CalendarException as e:
			return Response(json.encode({"status": "error"}), mimetype='application/json')

	elif request.method == 'PUT':
		try:
			events.user = current_user['id']
			events.id = request.form['id']
			events.startdate = request.form['start']
			events.enddate = request.form['end']

			return Response(events.update_date(), mimetype='application/json')
		except CalendarException as e:
			return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('calendar/<int:id>', methods=['GET','POST'])
@api_required
def calendar(id):
	try:
		current_user = decode_token(session['token'])['identity']
	except:	
		current_user = get_jwt_identity()
	if request.method == 'POST':
		try:
			checked = 'delete' in request.form
			if checked == True:
				events.user = current_user['id']
				events.id = id
				result = events.delete()
			else:
				events.user = current_user['id']
				events.id = id
				events.title = request.form['title']
				events.notes = request.form['notes']
				events.lieu = request.form['lieu']
				events.color = request.form['color']

				result = events.update_event()

			return Response(result, mimetype='application/json')
		except CalendarException as e:
			return Response(json.encode({"status": "error"}), mimetype='application/json')
