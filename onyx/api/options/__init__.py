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
from onyx.api.exceptions import *
from onyx.api.assets import Json
from onyx.config import get_config , get_path
import logging

logger = logging.getLogger()
json = Json()

"""
    Cette class can change option of Onyx

    Cette classe permet de gérer les options d'Onyx
"""
class Options:

    def __init__(self):
        self.user = None
        self.color = None
        self.lang = 'en-US'

    """
        Change the user color button

        Modifier la couleur d'un utilisateur
    """
    def set_account(self):
        try:
            query = UsersModel.User.query.filter_by(id=self.user).first()

            query.buttonColor = self.color

            db.session.add(query)
            db.session.commit()

            logger.info('User ' + query.username + ' updated successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('User update error : ' + str(e))
            raise OptionsException(str(e))
            return json.encode({"status":"error"})

    def change_lang(self):
        try:
            configPath = get_path('onyx')
            langConfig = get_config('onyx')
            langConfig.set('Base', 'lang', self.lang)
            with open(configPath, 'w') as configfile:
                langConfig.write(configfile)
            logger.info('Language update successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Language update error : ' + str(e))
            raise OptionsException(str(e))
            return json.encode({"status":"error"})
