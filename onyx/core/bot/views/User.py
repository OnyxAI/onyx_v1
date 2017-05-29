# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.exceptions import *
from onyxbabel import gettext
from flask_login import current_user
from onyx.api.user import *
from onyx.api.assets import Json
from .. import bot

users = User()
json = Json()

@bot.route('get_email')
def get_email(kwargs):

    scope = []

    for user_id in kwargs:
        e = {}
        users.id = user_id
        json.json = users.get_user()
        user = json.decode()
        e['%USER_EMAIL%'] = user['email']
        scope.append(e)

    result =  json.encode({"status":"success", "label":"user_email", "scope":scope})
    return result
