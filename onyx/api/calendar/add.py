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

def addEvent():

	color = request.form['color']
	enddate = request.form['end']
	startdate = request.form['start']
	title = request.form['title']
	notes = request.form['notes']
	lieu = request.form['lieu']

	query = CalendarModel.Calendar(idAccount=str(current_user.id),title=title , notes=notes , lieu=lieu , start=startdate, end=enddate ,color=color)
	db.session.add(query)
	db.session.commit()

	return redirect(url_for('core.calendars'))
