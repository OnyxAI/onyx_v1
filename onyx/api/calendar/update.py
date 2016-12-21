"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask_login import current_user
from onyx.core.models import *
from onyx.extensions import db
from flask import render_template, request, url_for, redirect
import json

def updateDate():
	query = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
	query.start = request.form['start']
	query.end = request.form['end']

	db.session.add(query)
	db.session.commit()

	return json.dumps({'status':'success'})



def updateEvent():
	
	checked = 'delete' in request.form
	if checked == True:
		delete = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
		db.session.delete(delete)
		db.session.commit()
		return redirect(url_for('core.calendars'))


	update = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
	update.title = request.form['title']
	update.notes = request.form['notes']
	update.lieu = request.form['lieu']
	update.color = request.form['color']
	db.session.add(update)
	db.session.commit()
	return redirect(url_for('core.calendars'))	

	
