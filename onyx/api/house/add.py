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

def add_house_db():
    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    postal = request.form['postal']
    country = request.form['country']
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    query = HouseModel.House(name=name,address=address,city=city,postal=postal,country=country,latitude=latitude,longitude=longitude)
    db.session.add(query)
    db.session.commit()
