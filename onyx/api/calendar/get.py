"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import render_template
from flask_login import current_user
from onyx.core.models import *
from onyx.extensions import db



def getEvent():
	events = []
	query = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(str(current_user.id)))

	for fetch in query:	
		e = {}
		e['id'] = fetch.id
		e['title'] = fetch.title
		e['notes'] = fetch.notes
		e['lieu'] = fetch.lieu
		e['start'] = fetch.start
		e['end'] = fetch.end
		e['color'] = fetch.color
		events.append(e)
		
	return render_template('calendar/index.html' , events=events)