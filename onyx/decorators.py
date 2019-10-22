# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import request , redirect , url_for , flash , g, current_app as app
from functools import wraps
from onyxbabel import gettext
from onyx.extensions import db

def admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if g.user.admin == 0:
			flash(gettext("You're not admin"), 'error')
			return redirect(url_for('core.index'))
		return f(*args, **kwargs)
	return decorated
