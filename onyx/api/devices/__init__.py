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

            return json.dumps(devices)
        except:
            raise Exception('Get Error')
            return json.dumps({"status":"error"})

    def add(self):
        try:
            query = DevicesModel.Device(name=self.name,identifier=self.identifier,protocol=self.protocol,service=self.service,room=self.room)

            db.session.add(query)
            db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Add Error')
            return json.dumps({"status":"error"})

    def delete(self):
        try:
            query = DevicesModel.Device.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Delete Error')
            return json.dumps({"status":"error"})
