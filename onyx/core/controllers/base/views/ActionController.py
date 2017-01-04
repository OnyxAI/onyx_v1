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
from flask import render_template, request, g
from flask.ext.login import login_required
from onyx.api.action import *


@core.route('action', methods=['POST'])
@login_required
def action():
	if request.method == 'POST':
		return get_action(request.form['q'])
