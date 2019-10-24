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


@pytest.mark.usefixtures('db', 'connected_app', 'connected_admin_app', 'user_test')
class Test_UserApi:

    def test_get_users(self, connected_app):
        response = connected_app.get('/api/users')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'

    def test_add_user(self, connected_app):
        response = connected_app.post('/api/user/register', {"email": "test@test.fr", "username": "Test", "password": "123456", "verifpassword": "123456"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

    def test_login_user(self, connected_app, user_test):
        response = connected_app.post('/api/user/login', {"email": "pepper@starkindustries.com", "password": "pepper1234"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json["status"] == "success"

    def test_delete_user_no_admin(self, connected_app, user_test):
        response = connected_app.get('/api/user/delete/{}'.format(user_test.id))
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json["status"] == "error"

    def test_delete_user_admin(self, connected_admin_app, user_test):
        response = connected_admin_app.get('/api/user/delete/{}'.format(user_test.id))
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}

    def test_manage_user_get(self, connected_admin_app, user_test):
        response = connected_admin_app.get('/api/user/manage/{}'.format(user_test.id))
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json["id"] != None

    def test_manage_user_post(self, connected_admin_app, user_test):
        response = connected_admin_app.post('/api/user/manage/{}'.format(user_test.id) , {"email": "test@starkindustries.com", "username": "test", "password": "test1234"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json["status"] == "success"

    def test_change_user(self, connected_admin_app, user_test):
        response = connected_admin_app.post('/api/user/change', {"email": "test@starkindustries.com", "username": "test", "password": "test1234", "lastpassword": "123456"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json["status"] == "success"
