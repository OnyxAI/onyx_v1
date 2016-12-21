"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask.ext.login import login_user
from flask import request , render_template , redirect , url_for , flash
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db
import hashlib



def loginUser():
	try:
		email = request.form['email']
		password = request.form['password'].encode('utf-8')
		registered_user = UsersModel.User.query.filter_by(email=email,password=hashlib.sha1(password).hexdigest()).first()
		if registered_user is None:
			flash(gettext('Incorrect email or password !'), 'error')
			return redirect(url_for('auth.login'))
		login_user(registered_user)
		registered_user.authenticated = True
		flash(gettext('You are now connected'), 'success')
		return redirect(request.args.get('next') or url_for('core.index'))
	except:
		email = request.form['email']
		password = request.form['password'].encode('utf-8')
		registered_user = UsersModel.User.query.filter_by(email=email,password=hashlib.sha1(password).hexdigest()).first()
		if registered_user is None:
			flash(gettext('Incorrect email or password !'), 'error')
			return redirect(url_for('auth.login'))
		login_user(registered_user)
		registered_user.authenticated = True
		flash(gettext('You are now connected'), 'success')
		return redirect(request.args.get('next') or url_for('core.index'))
	