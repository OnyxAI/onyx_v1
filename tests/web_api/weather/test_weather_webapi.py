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

@pytest.mark.usefixtures('db', 'connected_app')
class Test_WeatherApi:

    def test_weather_get_daily(self, connected_app):
        response = connected_app.post('/api/weather/daily', {"latitude": "50", "longitude": "2", "token": "test"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json != {"status": "error"}

    def test_weather_set_token(self, connected_app):
        response = connected_app.post('/api/weather/set_token', {"weather_token": "test"})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {"status": "success"}



