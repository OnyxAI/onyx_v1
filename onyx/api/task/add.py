"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import render_template, request , redirect , url_for
from flask.ext.login import current_user
from onyx.core.models import *
from onyx.extensions import db
import json

def addTask():
	text = request.form['text']	
	if not request.form['date']:
		task = TaskModel.Task(idAccount=str(current_user.id),text=text)
		db.session.add(task)
		db.session.commit()
		return json.dumps({'status':'success','calendar':'false','id':task.id})
	else:
		date = request.form['date'] + " 00:00:00"
		if request.form['calendar'] == "1":		
				
			calendar = CalendarModel.Calendar(idAccount=str(current_user.id), title=text , notes=text , start=date, end=date )
			db.session.add(calendar)
			db.session.commit()
			task = TaskModel.Task(idAccount=str(current_user.id),text=text,date=date , idCalendar=calendar.id)
			db.session.add(task)
			db.session.commit()
			return json.dumps({'status':'success','calendar':'true','id':task.id,'idCalendar':calendar.id})
		else:
			task = TaskModel.Task(idAccount=str(current_user.id),text=text,date=date)
			db.session.add(task)
			db.session.commit()
			return json.dumps({'status':'success','calendar':'false','id':task.id})