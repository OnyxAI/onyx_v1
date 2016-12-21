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



def getTask():
	tasks = []
	bdd = TaskModel.Task.query.filter(TaskModel.Task.idAccount.endswith(str(current_user.id)))
	for fetch in bdd:	
		e = {}
		e['id'] = fetch.id
		e['text'] = fetch.text
		e['date'] = fetch.date
		e['idCalendar'] = fetch.idCalendar
		tasks.append(e)
	return render_template('task/index.html' , tasks=tasks)