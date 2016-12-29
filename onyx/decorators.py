"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import request , redirect , url_for , flash , g
from functools import wraps
from onyxbabel import gettext
from onyx.extensions import db
from onyx.core.models import ConfigModel

def admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if g.admin == 0:
			flash(gettext("You're not admin"), 'error')
			return redirect(url_for('core.index'))
		return f(*args, **kwargs)
	return decorated

