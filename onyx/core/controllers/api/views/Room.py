# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import api
from flask import request
from onyx.decorators import api_required
from onyx.api.exceptions import RoomException
from onyx.decorators import admin_required
from onyx.api.room import Room
from onyx.api.assets import Json

json = Json()
room = Room()

@api.route('room')
@api_required
def get_room():
    try:
        return room.get()
    except RoomException:
        return json.encode({"status": "error"})

@api.route('room/add', methods=['POST'])
@api_required
def add_room():
    try:
        room.name = request.form['name']
        room.house = request.form['house']
        return room.add()
    except RoomException:
        return json.encode({"status": "error"})


@api.route('room/delete/<int:_id>')
@api_required
def delete_room(_id):
    try:
        room.id = _id
        return room.delete()
    except RoomException:
        return json.encode({"status": "error"})
