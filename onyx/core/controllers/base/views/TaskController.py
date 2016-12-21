"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask import request
from flask.ext.login import login_required
from onyx.api.task import *


@core.route('task', methods=['GET','POST','PUT'])
@login_required
def tasks():
	if request.method == 'GET':
		"""
		@api {get} /task Get Task Information
		@apiName getTask
		@apiGroup Task
		@apiPermission authenticated 

		@apiSuccess (200) {Object[]} tasks List of Task
		@apiSuccess (200) {Number} tasks.id Id of Task
		@apiSuccess (200) {Number} tasks.idCalendar Calendar Id of Task
		@apiSuccess (200) {String} tasks.text Text of Task
		@apiSuccess (200) {datetime} tasks.date Date of Task

		@apiError TaskNotFound No Task Found

		"""
		return getTask()

	elif request.method == 'POST':
		"""
		@api {post} /task Add Task
		@apiName addTask
		@apiGroup Task
		@apiPermission authenticated 

		@apiSuccess (200) {Number} tasks.idCalendar Calendar Id of Task
		@apiSuccess (200) {String} tasks.text Text of Task
		@apiSuccess (200) {datetime} tasks.date Date of Task

		@apiSuccess (200) {json} status Status
		@apiSuccess (200) {json} calendar Calendar Boolean
		@apiSuccess (200) {json} idCalendar Id of Calendar
		@apiSuccess (200) {json} id Id

		@apiSuccess (200) redirect Redirect to Task

		@apiError AlreadyExist This Task already Exist
		
		"""
		return addTask()

	elif request.method == 'PUT':
		"""
		@api {delete} /task Delete Task
		@apiName deleteTask
		@apiGroup Calendar
		@apiPermission authenticated 

		@apiParam {Number} id Id
		@apiParam {Number} idCalendar Id of Calendar Event

		@apiSuccess (200) redirect Redirect to Task
		
		"""
		return deleteTask()



@core.context_processor
def utility_processor():
	def split(str):
		try:
			pre = str.split(" ")
			return pre
		except:
			return ['Non Défini']
	return dict(split=split)