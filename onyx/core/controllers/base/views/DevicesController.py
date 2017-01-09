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
from onyx.api.devices import *
from onyxbabel import gettext

devices = Devices()

@core.route('devices/add', methods=['POST'])
@admin_required
@login_required
def add_device():
    try:
        devices.name = request.form['name']
        devices.identifier = request.form['identifier']
        devices.protocol = request.form['protocol']
        devices.service = request.form['service']
        devices.room = request.form['room']
        devices.add()
        flash(gettext('Devices Add'), 'success')
        return redirect(url_for('core.options'))
    except Exception:
		flash(gettext('An error has occured !'), 'error')
		return redirect(url_for('core.options'))


@core.route('devices/delete/<int:id>')
@admin_required
@login_required
def delete_device(id):
    try:
        devices.id = id
        devices.delete()
        flash(gettext('Devices Deleted'), 'success')
        return redirect(url_for('core.options'))
    except Exception:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.options'))
