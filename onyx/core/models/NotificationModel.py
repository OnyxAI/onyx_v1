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

class Notif(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String(255))
    link = db.Column(db.String(255))
    priority = db.Column(db.Integer())
    is_read = db.Column(db.Integer())
    icon = db.Column(db.String(64))
    icon_color = db.Column(db.String(64))
    user = db.Column(db.Integer())

    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
