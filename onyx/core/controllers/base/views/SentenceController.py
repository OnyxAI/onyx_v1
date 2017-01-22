# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import core
from flask import render_template, request, g, flash, redirect, url_for
from flask.ext.login import login_required
from onyxbabel import gettext
from onyx.api.sentences import *

actions = Sentences()

@core.route('sentence', methods=['POST'])
@login_required
def sentence():
	if request.method == 'POST':
		actions.text = request.form['q']
		actions.next = request.args['next']
		result = actions.get()
		print(result)
		json.json = result
		data = json.decode()
		if data['status'] == 'success':
			if data['type'] == 'notification':
				flash(data['text'], 'success')
				return redirect(url_for(data['next']))
			elif data['type'] == 'exec':
				flash(gettext('Action successfully performed ! ') , 'success')
				return redirect(url_for(data['next']))
		elif data['status'] == 'unknown command':
			flash(gettext('Unknown Command !') , 'error')
			return redirect(url_for(data['next']))
		else:
			flash(gettext('An error has occured !') , 'error')
			return redirect(url_for(data['next']))
