# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.assets import Json

json = Json()

class House:

    def __init__(self):
        self.id = None
        self.name = None
        self.address = None
        self.city = None
        self.postal = None
        self.country = None
        self.latitude = None
        self.longitude = None

    def get(self):
        try:
            query = HouseModel.House.query.all()
            houses = []
            for fetch in query:
                house = {}
                house['id'] = fetch.id
                house['name'] = fetch.name
                house['address'] = fetch.address
                house['city'] = fetch.city
                house['postal'] = fetch.postal
                house['country'] = fetch.country
                house['latitude'] = fetch.latitude
                house['longitude'] = fetch.longitude
                houses.append(house)

            return json.encode(houses)
        except:
            raise Exception('Get Error')
            return json.encode({"status":"error"})

    def add(self):
        try:
            query = HouseModel.House(name=self.name,address=self.address,city=self.city,postal=self.postal,country=self.country,latitude=self.latitude,longitude=self.longitude)

            db.session.add(query)
            db.session.commit()
            return json.encode({"status":"success"})
        except:
            raise Exception('Add Error')
            return json.encode({"status":"error"})

    def delete(self):
        try:
            query = HouseModel.House.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()
            return json.encode({"status":"success"})
        except:
            raise Exception('Delete Error')
            return json.encode({"status":"error"})
