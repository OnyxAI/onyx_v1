"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask import request , render_template , redirect , url_for , flash
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db
import hashlib



def registerUser():
	try:
		if request.form['password'] == request.form['verifpassword']:
			hashpass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
			user = UsersModel.User(admin=0 , username=request.form['username'] , password=hashpass, email=request.form['email'])
			db.session.add(user)
			db.session.commit()
			flash(gettext('Account Added !') , 'success')
			return redirect(url_for('auth.hello'))
		else:
			flash(gettext('Passwords are not same !' ), 'error')
			return redirect(url_for('auth.register'))
	except:
		db.session.rollback()
		flash(gettext('A Account with this informations already exist !') , 'error')
		return redirect(url_for('auth.hello'))