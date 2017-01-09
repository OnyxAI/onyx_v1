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

class Machine:

    def __init__(self):
        self.id = None
        self.name = None
        self.house = None
        self.room = None
        self.host = None


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

            return json.dumps(machines)
        except:
            raise Exception('Get Error')
            return json.dumps({"status":"error"})

    def add(self):
        try:
            query = MachineModel.Machine(name=self.name,house=self.house,room=self.room,host=self.host)

            db.session.add(query)
            db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Add Error')
            return json.dumps({"status":"error"})

    def delete(self):
        try:
            query = MachineModel.Machine.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Delete Error')
            return json.dumps({"status":"error"})
