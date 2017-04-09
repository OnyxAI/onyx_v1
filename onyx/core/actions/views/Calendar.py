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
from flask_login import current_user
from onyxbabel import gettext
from onyx.api.assets import Json
from .. import action
from onyx.api.calendar import *

events = Calendar()
json = Json()

@action.route('calendar/meet')
def calendar_meet():
    events.user = current_user.id
    json.json = events.get_meet()
    data = json.decode()
    meeting = str(len(data))
    return gettext('You have ') + meeting + gettext(' events today !')
