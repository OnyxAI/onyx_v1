# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.core.models import *
from flask_login import current_user
from onyx.extensions import db
from onyx.api.assets import Json
from onyx.api.exceptions import *
import logging

logger = logging.getLogger()
json = Json()

class Notification:

    def __init__(self):
        self.id = None
        self.text = None
        self.link = None
        self.priority = 0
        self.is_read = 0
        self.icon = 'fa-bell'
        self.icon_color = 'blue darken-1'
        self.user = None

    def get_all(self):
        query = NotificationModel.Notif.query.filter(NotificationModel.Notif.user.endswith(current_user.id))
        notifs = []

        for fetch in query:
            e = {}
            e['id'] = fetch.id
            e['title'] = fetch.title
            e['text'] = fetch.text
            e['link'] = fetch.link
            e['priority'] = fetch.priority
            e['is_read'] = fetch.is_read
            e['icon'] = fetch.icon
            e['icon_color'] = fetch.icon_color
            e['user'] = fetch.user
            notifs.append(e)

        return json.encode(notifs)

    def get(self):
        query = NotificationModel.Notif.query.filter_by(user=current_user.id, is_read=0).all()
        notifs = []

        for fetch in query:
            e = {}
            e['id'] = fetch.id
            e['title'] = fetch.title
            e['text'] = fetch.text
            e['link'] = fetch.link
            e['priority'] = fetch.priority
            e['is_read'] = fetch.is_read
            e['icon'] = fetch.icon
            e['icon_color'] = fetch.icon_color
            e['user'] = fetch.user
            notifs.append(e)

        return json.encode(notifs)

    def notify(self):
        query = NotificationModel.Notif(title=self.title, text=self.text, link=self.link, priority=self.priority, is_read=self.is_read, icon=self.icon, icon_color=self.icon_color, user=self.user)

        db.session.add(query)
        db.session.commit()
        logger.info('Notification ' + query.title + ' added successfully')

    def mark_read(self):
        query = NotificationModel.Notif.query.filter_by(user=current_user.id, is_read=0).all()

        for fetch in query:
            fetch.is_read = 1
            db.session.add(fetch)
            db.session.commit()
        logger.info('Notification mark as read successfully')

    def delete(self):
        query = NotificationModel.Notif.query.filter_by(id=self.id).first()

        db.session.delete(query)
        db.session.commit()
        logger.info('Delete notification successfully')
