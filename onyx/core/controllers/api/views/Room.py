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
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from onyx.decorators import admin_required
from onyx.api.room import *
from onyxbabel import gettext

room = Room()

@api.route('room')
@admin_required
@login_required
def get_room():
    return room.get()

@api.route('room/add', methods=['POST'])
@admin_required
@login_required
def add_room():
    try:
        room.name = request.form['name']
        room.house = request.form['house']
        return room.add()
    except Exception:
		return room.add()


@api.route('room/delete/<int:id>')
@admin_required
@login_required
def delete_room(id):
    try:
        room.id = id
        return room.delete()
    except Exception:
        return room.delete()
