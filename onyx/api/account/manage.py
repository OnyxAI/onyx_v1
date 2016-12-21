"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import request , render_template, flash, redirect, url_for
from onyx.core.models import *
from onyx.extensions import db
from flask.ext.login import current_user
from onyxbabel import gettext
import hashlib


def manageAccount():
	try:
		bdd = UsersModel.User.query.all()
		resultIdRow = []
		for myusers in bdd:
			resultIdRow.append(myusers) 
			resultId = resultIdRow
		return render_template('account/manage.html' , id=resultId )
	except:
		return render_template('account/manage.html')

def manageUser(id):
	try:
		user = UsersModel.User.query.filter_by(id=id).first()
		if not request.form['username']:
			user.username = user.username
		else:
			user.username = request.form['username']
		if not request.form['email']:
			user.email = user.email
		else:
			user.email = request.form['email']
		if not request.form['password']:
			user.password = user.password
		else:
			user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
		db.session.add(user)
		db.session.commit()
		flash(gettext('Account changed !') , 'success')
		return redirect(url_for('auth.account_manage'))
	except:
		flash(gettext('An error has occurred !') , 'error')
		return redirect(url_for('auth.account_manage'))