# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.extensions import db

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    address = db.Column(db.String(256))
    city = db.Column(db.String(256))
    postal = db.Column(db.String(256))
    country = db.Column(db.String(256))
    latitude = db.Column(db.String(256))
    longitude = db.Column(db.String(256))
