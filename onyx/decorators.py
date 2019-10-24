# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import redirect , url_for , flash , g, session, Response
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request, decode_token
from onyx.api.user import User
from onyx.api.assets import Json
from functools import wraps
from onyxbabel import gettext

json = Json()
user_api = User()

def admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if g.user.admin == 0:
			flash(gettext("You're not admin"), 'error')
			return redirect(url_for('core.index'))
		return f(*args, **kwargs)
	return decorated

def api_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		try:
			decoded = decode_token(session['token'])
			return f(*args, **kwargs)
		except:
			verify_jwt_in_request()
			return f(*args, **kwargs)
	return decorated

def admin_api_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		current_user = get_jwt_identity()
		if current_user['admin'] == '0':
			return Response(json.encode({"status": "error", "message": "You're not admin"}), mimetype='application/json')
		return f(*args, **kwargs)
	return decorated
