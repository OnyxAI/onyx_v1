# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask.ext.login import current_user
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.assets import Json

json = Json()

class Options:

    def __init__(self):
        self.color = None
        self.lang = None

    def set_account(self):
        try:
            query = UsersModel.User.query.filter_by(id=current_user.id).first()

            query.buttonColor = self.color
            query.lang = self.lang

            db.session.add(query)
            db.session.commit()
            return json.encode({"status":"success"})
        except:
            raise Exception('Error set account')
            return json.encode({"status":"error"})
