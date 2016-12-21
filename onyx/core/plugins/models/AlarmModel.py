"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ...extensions import db


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(64))
    ring = db.Column(db.String(64))
    heure = db.Column(db.String(120))
    active = db.Column(db.String(64))
    test = db.Column(db.String(64))
 

    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  
