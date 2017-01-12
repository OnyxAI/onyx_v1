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

class Devices:

    def __init__(self):
        self.id = None
        self.name = None
        self.identifier = None
        self.protocol = None
        self.service = None
        self.room = None


    def get(self):
        try:
            query = DevicesModel.Device.query.all()
            devices = []
            for fetch in query:
                device = {}
                device['id'] = fetch.id
                device['name'] = fetch.name
                device['identifier'] = fetch.identifier
                device['protocol'] = fetch.protocol
                device['service'] = fetch.service
                device['room'] = fetch.room
                devices.append(device)
            return json.encode(devices)
        except Exception as e:
            logger.error('Getting devices error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def add(self):
        try:
            query = DevicesModel.Device(name=self.name,identifier=self.identifier,protocol=self.protocol,service=self.service,room=self.room)

            db.session.add(query)
            db.session.commit()
            logger.info('New Device : ' + query.name)
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Error device add : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def delete(self):
        try:
            query = DevicesModel.Device.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()
            logger.info('Device ' + query.name + ' deleted successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Device delete error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})
