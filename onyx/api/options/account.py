"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask import redirect , url_for , flash , request
from flask.ext.login import current_user
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db

def setAccount():
	try:
		user = UsersModel.User.query.filter_by(username=current_user.username).first()
		if not request.form['color']:
			user.buttonColor = current_user.buttonColor
		else:
			user.buttonColor = request.form['color']
		if not request.form['lang']:
			user.lang = current_user.lang
		else:
			user.lang = request.form['lang']
		db.session.add(user)
		db.session.commit()
		flash(gettext('Account changed successfully' ), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext("You don't enter param"), 'success')
		return redirect(url_for('core.options'))