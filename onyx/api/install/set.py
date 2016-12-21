"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import flash, request, redirect, url_for
from flask.ext.login import login_user, current_user, LoginManager
from onyxbabel import gettext as _
from onyx.extensions import db, login_manager
from onyx.core.models import *
import os
import hashlib


def setInstall():
	try:
		hashpass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
		user = UsersModel.User(admin=1, username=request.form['username'] , password=hashpass, email=request.form['email'])
		db.session.add(user)
		db.session.commit()
		login_user(user)
	except:
		flash('Une erreur est survenue !' , 'error')
		return redirect(url_for('install.index'))
	flash('Onyx a bien été installé !' , 'success')
	return redirect(url_for("install.finish"))