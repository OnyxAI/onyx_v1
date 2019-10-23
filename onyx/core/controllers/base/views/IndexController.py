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
from flask import render_template
from flask_login import login_required, current_user
from onyx.api.assets import Json
from onyx.api.widgets import Widgets

json = Json()
box = Widgets()

@core.route('/')
@login_required
def index():
    box.user = current_user.id
    boxs = json.decode(box.get())

    return render_template('index/index.html', boxs=boxs)
