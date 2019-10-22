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
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required
from onyx.api.exceptions import *
from onyx.decorators import admin_required
from onyx.api.room import *
from onyxbabel import gettext

room = Room()

@api.route('room')
@admin_required
@login_required
def get_room():
    """
    @api {get} /room Request Rooms Information
    @apiName getRoom
    @apiGroup Room
    @apiPermission authenticated

    @apiSuccess (200) {Object[]} rooms List of Rooms
    @apiSuccess (200) {Number} rooms.id Id of Rooms
    @apiSuccess (200) {String} rooms.house House of Rooms
    @apiSuccess (200) {String} rooms.name Name of Rooms

    @apiError RoomNotFound No Room Found

    """
    return room.get()

@api.route('room/add', methods=['POST'])
@admin_required
@login_required
def add_room():
    """
    @api {post} /room/add Add Room
    @apiName addRoom
    @apiGroup Room
    @apiPermission authenticated

    @apiParam {String} house House of Room
    @apiParam {String} name Name of Room

    @apiSuccess (200) redirect Redirect to Option

    @apiError AlreadyExist This Room already Exist

    """
    try:
        room.name = request.form['name']
        room.house = request.form['house']
        return room.add()
    except RoomException:
        return room.add()


@api.route('room/delete/<int:id>')
@admin_required
@login_required
def delete_room(id):
    """
    @api {delete} /room/delete Delete Room
    @apiName deleteRoom
    @apiGroup Room
    @apiPermission authenticated

    @apiParam {Number} id Id of Room

    @apiSuccess (200) delete Room Deleted

    @apiError RoomNotFound No Room Found

    """
    try:
        room.id = id
        return room.delete()
    except RoomException:
        return room.delete()
