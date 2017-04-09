# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.assets import *
import json
import pytest
import os.path
import onyx

from time import strftime

json_test = Json()

class Test_Json:

    def test_decode_json(self):
        data = json.dumps({"status":"success"})
        json_test.json = data
        json_decoded = json_test.decode()

        assert json_decoded['status'] == "success"

    def test_encode_json(self):
        data = {"status":"success"}
        encoded = json_test.encode(data)

        json_decoded = json.loads(encoded)

        assert json_decoded['status'] == "success"

    def test_url_json(self):
        json_test.url = 'http://date.jsontest.com/'
        decoded = json_test.decode_url()

        assert decoded['date'] == strftime("%m-%d-%Y")

    def test_decode_path_json(self):
        path = os.path.abspath(os.path.join(onyx.__path__[0], os.pardir))
        path += "/tests/assets/json/test.json"

        json_test.path = path
        json_decoded = json_test.decode_path()

        assert json_decoded['status'] == "success"
