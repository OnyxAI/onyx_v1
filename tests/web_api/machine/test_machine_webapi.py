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
class Test_MachineApi:

    def test_get_machines(self, connected_app):
        response = connected_app.get('/api/machine')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json != {"status": "error"}

    def test_add_machine(self, connected_app):
        response = connected_app.post('/api/machine/add', {"name": "My Machine", "house": 1, "room": 1, "host": "localhost"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

    def test_delete_machine(self, connected_app, db):
        delete_machine = MachineModel.Machine(name='boo', house='foo', room='room', host='localhost')
        db.session.add(delete_machine)
        db.session.commit()

        response = connected_app.get('/api/machine/delete/{}'.format(delete_machine.id))
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

