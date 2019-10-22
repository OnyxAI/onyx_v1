# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import core
from flask import request,render_template, url_for,redirect, current_app as app
from flask_login import login_required
from onyx.api.assets import Json
from onyx.api.widgets import *

json = Json()
box = Widgets()

@core.route('/')
@login_required
def index():
    json.json = box.get()
    boxs = json.decode()
    return render_template('index/index.html', boxs=boxs)
