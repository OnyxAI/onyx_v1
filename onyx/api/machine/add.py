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
from flask import request

def add_machine_db():
    name = request.form['name']
    house = request.form['house']
    room = request.form['room']
    host = request.form['host']


    query = MachineModel.Machine(name=name,house=house,room=room,host=host)
    db.session.add(query)
    db.session.commit()
