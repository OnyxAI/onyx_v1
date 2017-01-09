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
import json

class Room:

    def __init__(self):
        self.id = None
        self.name = None
        self.house = None

    def get(self):
        try:
            query = RoomModel.Room.query.all()
            return json.dumps(list(query))
        except:
            query = RoomModel.Room.query.all()
            rooms = []
            for fetch in query:
                room = {}
                room['id'] = fetch.id
                room['name'] = fetch.name
                room['house'] = fetch.house
                rooms.append(room)

            return json.dumps(rooms)

    def add(self):
        try:
            query = RoomModel.Room(name=self.name,house=self.house)

            db.session.add(query)
            db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Add Error')
            return json.dumps({"status":"error"})

    def delete(self):
        try:
            query = RoomModel.Room.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Delete Error')
            return json.dumps({"status":"error"})
