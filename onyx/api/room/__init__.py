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
from onyx.api.exceptions import *
import logging

logger = logging.getLogger()
json = Json()

"""
    This class allows to manage the rooms of the house

    Cette classe permet de gérér les pièces de la maison
"""
class Room:

    def __init__(self):
        self.id = None
        self.name = None
        self.house = None

    """
        Get all rooms

        Récupérer toutes les pièces
    """
    def get(self):
        try:
            query = RoomModel.Room.query.all()
            rooms = []
            for fetch in query:
                room = {}
                room['id'] = fetch.id
                room['name'] = fetch.name
                room['house'] = fetch.house
                rooms.append(room)

            return json.encode(rooms)
        except Exception as e:
            logger.error('Getting room error : ' + str(e))
            raise RoomException(str(e))
            return json.encode({"status":"error"})

    """
        Add a new room

        Ajouter une nouvelle pièce
    """
    def add(self):
        try:
            query = RoomModel.Room(name=self.name,house=self.house)

            db.session.add(query)
            db.session.commit()
            logger.info('Room ' + query.name + ' added successfuly')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Room add error : ' + str(e))
            raise RoomException(str(e))
            return json.encode({"status":"error"})

    """
        Delete a room

        Supprimer une pièce
    """
    def delete(self):
        try:
            query = RoomModel.Room.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()
            logger.info('Room ' + query.name + ' deleted successfuly')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Room delete error : ' + str(e))
            raise RoomException(str(e))
            return json.encode({"status":"error"})
