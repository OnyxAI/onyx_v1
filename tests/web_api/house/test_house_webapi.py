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
class Test_HouseApi:

    def test_get_houses(self, connected_app):
        response = connected_app.get('/api/house')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'

    def test_add_house(self, connected_app):
        response = connected_app.post('/api/house/add', {"name": "My House", "address": "My Address", "city": "My City", "postal": "59000", "country": "FR", "latitude": "52", "longitude": "2"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

    def test_delete_house(self, connected_app, db):
        delete_house = HouseModel.House(name='boo', address='foo', city='My City', postal='59000', country='FR', latitude='50', longitude='2')
        db.session.add(delete_house)
        db.session.commit()

        response = connected_app.get('/api/house/delete/{}'.format(delete_house.id))
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

