"""
Onyx Project
http://onyx^project.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask import render_template, request
from flask.ext.login import login_required


@core.route('app')
@login_required
def app():
	return render_template('app/index.html')
