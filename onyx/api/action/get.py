"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask import g, redirect, flash, url_for
from onyx.api.assets import decodeJSON
from onyxbabel import gettext
from onyx.api.action import get_event

def get_action(text):
	try:
		data = decodeJSON.decode_action(g.lang)
		e = 0
		while e < len(data):
			if data[e]['text'] == text:
				return get_event.get_event(data[e]['label'],data[e]['api'],data[e]['type'],'next')
			e+=1
		flash(gettext('This is not a Onyx action !'), 'error')
		return redirect(url_for('core.index'))
	except:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.index'))