# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import api
from flask import request
from flask.ext.login import login_required
from onyx.decorators import admin_required
from onyx.api.devices import *
from onyxbabel import gettext

devices = Devices()

@api.route('devices')
@admin_required
@login_required
def get_device():
    return devices.get()

@api.route('devices/add', methods=['POST'])
@admin_required
@login_required
def add_device():
    try:
        devices.name = request.form['name']
        devices.identifier = request.form['identifier']
        devices.protocol = request.form['protocol']
        devices.service = request.form['service']
        devices.room = request.form['room']
        return devices.add()
    except Exception:
		return devices.add()


@api.route('devices/delete/<int:id>')
@admin_required
@login_required
def delete_device(id):
    try:
        devices.id = id
        return devices.delete()
    except Exception:
        return devices.delete()
