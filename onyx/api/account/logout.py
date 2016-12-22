"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask.ext.login import logout_user
from flask import request , render_template , redirect , url_for , flash
from onyxbabel import gettext
from onyx.extensions import db, login_manager
from onyx.core.models import *

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))


def logoutUser():
	login_manager.login_view = 'auth.hello'
	logout_user()
	flash(gettext('You are now log out' ), 'info')
	return redirect(url_for('auth.hello'))
	