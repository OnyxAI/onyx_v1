# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.extensions import db


class Navbar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64))
    url = db.Column(db.String(64))
    tooltip = db.Column(db.String(64))
    pourcentage = db.Column(db.String(64))
    fa = db.Column(db.String(64))

    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
