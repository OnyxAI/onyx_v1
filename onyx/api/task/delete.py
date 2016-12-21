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


def deleteTask():
	if request.form['idCalendar'] == "false":
		delete = TaskModel.Task.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
		db.session.delete(delete)
		db.session.commit()
	else:
		delete = TaskModel.Task.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
		db.session.delete(delete)
		db.session.commit()
		deleteCalendar = CalendarModel.Calendar.query.filter_by(id=request.form['idCalendar'],idAccount=str(current_user.id)).first()
		db.session.delete(deleteCalendar)
		db.session.commit()
	return redirect(url_for('core.tasks'))