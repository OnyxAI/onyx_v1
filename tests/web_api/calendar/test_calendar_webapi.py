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
from onyx.core.models import *
from flask import session

@pytest.mark.usefixtures('db', 'connected_app')
class Test_CalendarApi:

    def test_calendar_get(self, connected_app):
        response = connected_app.get('/api/calendar')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == []

    def test_calendar_post(self, connected_app):
        response = connected_app.post('/api/calendar', {"title": "test", "notes": "test", "lieu": "test", "start": "2019-10-02 00:00:00", "end": "2019-10-03 00:00:00", "color": "#0071c5"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json['status'] == 'success'

    def test_calendar_put(self, connected_app, db):
        query = CalendarModel.Calendar(user=1,\
                                           title="test",\
                                           notes="test",\
                                           lieu="test",\
                                           start="2019-10-02 00:00:00",\
                                           end="2019-10-03 00:00:00",\
                                           color="#0071c5")
        db.session.add(query)
        db.session.commit()

        response = connected_app.put('/api/calendar', {"id": query.id, "start": "2019-10-02 00:00:00", "end": "2019-10-04 00:00:00"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json['status'] == 'success'

    def test_calendar_update(self, connected_app, db):
        query = CalendarModel.Calendar(user=1,\
                                           title="test",\
                                           notes="test",\
                                           lieu="test",\
                                           start="2019-10-02 00:00:00",\
                                           end="2019-10-03 00:00:00",\
                                           color="#0071c5")
        db.session.add(query)
        db.session.commit()

        response = connected_app.post('/api/calendar/{}'.format(query.id), {"delete": False, "title": "test", "notes": "test", "lieu": "test", "color": "#0071c5"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json['status'] == 'success'

    def test_calendar_delete(self, connected_app, db):
        query = CalendarModel.Calendar(user=1,\
                                           title="test",\
                                           notes="test",\
                                           lieu="test",\
                                           start="2019-10-02 00:00:00",\
                                           end="2019-10-03 00:00:00",\
                                           color="#0071c5")
        db.session.add(query)
        db.session.commit()

        response = connected_app.post('/api/calendar/{}'.format(query.id), {"delete": True, "title": "test", "notes": "test", "lieu": "test", "color": "#0071c5"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json['status'] == 'success'



