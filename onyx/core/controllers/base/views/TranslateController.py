"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required

@core.route('translate')
@login_required
def translate():
	return render_template('translate/index.html')
