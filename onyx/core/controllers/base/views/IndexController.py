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
from flask import request,render_template, url_for,redirect, current_app as app, make_response, jsonify
from flask.ext.login import login_required
from multiprocessing import Process
from onyx.core.controllers.api.views.User import get_users



@core.route('/')
@login_required
def index():
    return render_template('index/index.html')
