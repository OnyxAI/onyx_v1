# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.room import *
from onyx.core.models import *
import json
import pytest

room = Room()

@pytest.mark.usefixtures('db')
class Test_Room:

    def test_get_rooms(self):
        delete_room = RoomModel.Room(name='boo', house='foo')
        db.session.add(delete_room)
        db.session.commit()

        result = json.loads(room.get())

        assert result[0]['name'] == 'boo'

    def test_add_rooms(self):
        room.house = 'foo'
        room.name = 'boo'
        result = json.loads(room.add())

        assert result['status'] == 'success'

    def test_delete_rooms(self, db):
        delete_room = RoomModel.Room(name='boo', house='foo')
        db.session.add(delete_room)
        db.session.commit()

        room.id = delete_room.id
        result = json.loads(room.delete())
        assert result['status'] == 'success'
