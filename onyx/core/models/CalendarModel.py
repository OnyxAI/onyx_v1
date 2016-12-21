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
from onyx.extensions import db


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idAccount = db.Column(db.String(64))
    title = db.Column(db.String(64))
    lieu = db.Column(db.String(255))
    notes = db.Column(db.String(255))
    start = db.Column(db.String(64))
    end = db.Column(db.String(64))
    color = db.Column(db.String(64))
    allday = db.Column(db.String(64))


    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  
