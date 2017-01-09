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
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from onyx.decorators import admin_required
from onyx.api.navbar import *


@core.route('navbar/update' , methods=['POST'])
@login_required
def update_navbar():
	set_navbar(request.form['last'],request.form['new'])
	flash(gettext('Modified'), 'success')
	return redirect(url_for('core.options'))
