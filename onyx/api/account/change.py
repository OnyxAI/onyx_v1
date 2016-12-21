"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import request , render_template, flash, redirect, url_for
from flask.ext.login import current_user
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db
import hashlib

def changeAccount():
	try:
		user = UsersModel.User.query.filter_by(username=current_user.username).first()
		lastpassword = user.password
		if hashlib.sha1(request.form['lastpassword'].encode('utf-8')).hexdigest() == lastpassword:
			if not request.form['username']:
				user.username = current_user.username
			else:
				user.username = request.form['username']
			if not request.form['email']:
				user.email = current_user.email
			else:
				user.email = request.form['email']
			if not request.form['password']:
				user.password = current_user.password
			else:
				user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
			db.session.add(user)
			db.session.commit()
			flash(gettext('Account changed successfully' ), 'success')
			return redirect(url_for('auth.change_account'))
		else:
			flash(gettext('Passwords are not same !' ), 'error')
			return redirect(url_for('auth.change_account'))
	except:
		flash(gettext('Another user use data') , 'error')
		return redirect(url_for('auth.change_account'))