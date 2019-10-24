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
from flask import request, Response
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
        return Response(room.get(), mimetype='application/json')
    except RoomException:
        return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('room/add', methods=['POST'])
@api_required
def add_room():
    try:
        room.name = request.form['name']
        room.house = request.form['house']
        
        return Response(room.add(), mimetype='application/json')
    except RoomException:
        return Response(json.encode({"status": "error"}), mimetype='application/json')


@api.route('room/delete/<int:_id>')
@api_required
def delete_room(_id):
    try:
        room.id = _id
        return Response(room.delete(), mimetype='application/json')
    except RoomException:
        return Response(json.encode({"status": "error"}), mimetype='application/json')
