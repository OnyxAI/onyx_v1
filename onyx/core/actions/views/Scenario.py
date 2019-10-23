# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""


from onyx.api.exceptions import *
from flask_login import current_user
from onyx.api.notification import Notification
from onyx.api.assets import Json
from onyx.api.events import Event
from .. import action

events = Event()
json = Json()
notif = Notification()

@action.route('notification')
def notification(param):
    try:
        json.json = param
        params = json.decode()

        notif.user = current_user.id
        notif.title = params[0]
        notif.text = params[1]
        notif.priority = params[2]
        notif.icon = params[3]
        notif.icon_color = params[4]
        notif.user = params[5]
        notif.notify()

        return json.encode({"status":"success"})
    except:
        return json.encode({"status":"error"})

@action.route('event')
def event(param):
    try:
        json.json = param
        params = json.decode()

        events.code = params[0]
        events.template = params[1]
        events.new()

        return json.encode({"status":"success"})
    except:
        return json.encode({"status":"error"})
