# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import json
import pytest
from flask import session
from onyx.core.models import *


@pytest.mark.usefixtures('db', 'connected_app', 'connected_admin_app')
class Test_RoomApi:

    def test_get_rooms(self, connected_app):
        response = connected_app.get('/api/room')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json != {"status": "error"}

    def test_add_room(self, connected_app):
        response = connected_app.post('/api/room/add', {"name": "My Room", "house": 1})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

    def test_delete_room(self, connected_app, db):
        delete_room = RoomModel.Room(name='boo', house='foo')
        db.session.add(delete_room)
        db.session.commit()

        response = connected_app.get('/api/room/delete/{}'.format(delete_room.id))
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

