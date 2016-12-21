"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import request , render_template, flash, redirect, url_for
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db

def deleteAccount(id_delete):
	try:
		delete = UsersModel.User.query.filter_by(id=id_delete).first()
		db.session.delete(delete)
		db.session.commit()
		deleteCalendar = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(str(id_delete)))
		for fetch in deleteCalendar:
			deleteEvent = CalendarModel.Calendar.query.filter_by(id=fetch.id).first()
			db.session.delete(deleteEvent)
			db.session.commit()
		deleteTask = TaskModel.Task.query.filter(TaskModel.Task.idAccount.endswith(str(id_delete)))
		for fetch in deleteTask:
			deleteEventTask = TaskModel.Task.query.filter_by(id=fetch.id).first()
			db.session.delete(deleteEventTask)
			db.session.commit()
		flash(gettext('Account deleted !') , 'success')
		return redirect(url_for('auth.account_manage'))
	except:
		flash(gettext('An error has occurred !') , 'error')
		return redirect(url_for('auth.account_manage'))