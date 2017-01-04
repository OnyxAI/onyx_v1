# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import redirect, url_for, flash
import importlib

def get_event(label,api,type_event,next):
	if type_event == 'notification':
		m = importlib.import_module('onyx.api.'+api)
		func = getattr(m,label)
		retur = func()
		flash(retur,'success')
		return redirect(url_for('core.index'))
