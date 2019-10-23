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

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    template = db.Column(db.String(256))
    active = db.Column(db.Integer())
    event = db.Column(db.String(256))
    action = db.Column(db.String(256))
    action_param = db.Column(db.String(256))
    user = db.Column(db.Integer())
