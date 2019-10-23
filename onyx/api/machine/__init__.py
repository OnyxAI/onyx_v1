# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.util.log import getLogger

logger = getLogger('Machine')
json = Json()

"""
    Allows to manage the different instances of Onyx

    Permet de gérer les différentes instances d'Onyx
"""
class Machine:

    def __init__(self):
        self.id = None
        self.name = None
        self.house = None
        self.room = None
        self.host = None

    """
        Getting all machine

        Récupération de toutes les machines
    """
    def get(self):
        try:
            query = MachineModel.Machine.query.all()
            machines = []
            for fetch in query:
                machine = {}
                machine['id'] = fetch.id
                machine['name'] = fetch.name
                machine['house'] = fetch.house
                machine['room'] = fetch.room
                machine['host'] = fetch.host

                machines.append(machine)

            return json.encode(machines)
        except Exception as e:
            logger.error('Getting machine error : ' + str(e))
            raise GetException(str(e))

    """
        Add a new machine

        Ajout d'une nouvelle machine
    """
    def add(self):
        try:
            query = MachineModel.Machine(name=self.name,house=self.house,room=self.room,host=self.host)

            db.session.add(query)
            db.session.commit()
            
            logger.info('Machine ' + query.name + ' added successfuly')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.info('Machine add error : ' + str(e))
            raise MachineException(str(e))

    """
        Delete a machine

        Supprime une machine
    """
    def delete(self):
        try:
            query = MachineModel.Machine.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()

            logger.info('Machine ' + query.name + ' deleted successfuly')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Machine delete error : ' + str(e))
            raise MachineException(str(e))
