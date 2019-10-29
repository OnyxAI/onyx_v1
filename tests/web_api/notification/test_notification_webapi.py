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
class Test_NotificationApi:

    def test_get_notifications(self, connected_app):
        response = connected_app.get('/api/notification/all')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json != {"status": "error"}

    def test_get_unread_notifications(self, connected_app):
        response = connected_app.get('/api/notification/unread')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json != {"status": "error"}

    def test_mark_read_notifications(self, connected_app):
        response = connected_app.get('/api/notification/mark_read')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

    def test_add_notification(self, connected_app):
        response = connected_app.post('/api/notification', {"title": "My Notification", "text": "text", "priority": 1, "icon": "fa-user", "icon_color": "blue"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

    def test_delete_notification(self, connected_app, db):

        delete_notification = NotificationModel.Notif(title="Title", text="text", priority=1, icon="fa-user", icon_color="blue", user=1)
        db.session.add(delete_notification)
        db.session.commit()

        response = connected_app.get('/api/notification/delete/{}'.format(delete_notification.id))
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

