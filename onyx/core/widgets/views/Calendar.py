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
from onyx.api.assets import Json
from .. import widgets
from flask import render_template
from onyx.api.calendar import *

events = Calendar()
json = Json()

@widgets.route('calendar')
def calendar():
    json.json = events.get()
    events_list = json.decode()
    return render_template('widgets/calendar.html', events=events_list)

@widgets.context_processor
def utility_processor():
    def split(str):
        return str.split(" ")
    return dict(split=split)
