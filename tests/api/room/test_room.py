# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.house import *
from onyx.core.models import *
import json
import pytest

house = House()

@pytest.mark.usefixtures('db')
class Test_House:

    def test_get_rooms(self):
        get_house = HouseModel.House(name='My House', address='12 place Mandela', city='London', postal='4450', country='England', latitude='52.1243', longitude='2.1452' )
        db.session.add(get_house)
        db.session.commit()

        result = json.loads(house.get())

        assert result[0]['name'] == 'My House'

    def test_add_houses(self):
        house.name = 'My House'
        house.address = '12 place Mandela'
        house.city = 'London'
        house.postal = '4450'
        house.country = 'England'
        house.latitude = '52.1243'
        house.longitude = '2.1452'
        result = json.loads(house.add())

        assert result['status'] == 'success'

    def test_delete_houses(self, db):
        delete_house = HouseModel.House(name='My House', address='12 place Mandela', city='London', postal='4450', country='England', latitude='52.1243', longitude='2.1452' )
        db.session.add(delete_house)
        db.session.commit()

        house.id = delete_house.id
        result = json.loads(house.delete())
        assert result['status'] == 'success'
