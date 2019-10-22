# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
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
from onyx.util.log import getLogger

logger = getLogger('Notification')
json = Json()

"""
    Manages the notification part of Onyx

    Gère la partie notification d'Onyx
"""
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

    """
        Get all notifications of a user

        Récupère toutes les notifications d'un utilisateur
    """
    def get_all(self):
        try:
            query = NotificationModel.Notif.query.filter(NotificationModel.Notif.user.endswith(self.user))
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
        except Exception as e:
            logger.error('Notification Get error : ' + str(e))
            raise NotifException(str(e))

    """
        Get all unread notifications of a user

        Récupère toutes les notifications non lues d'un utilisateur
    """
    def get(self):
        try:
            query = NotificationModel.Notif.query.filter_by(user=self.user, is_read=0).all()
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
        except Exception as e:
            logger.error('Notification Get error : ' + str(e))
            raise NotifException(str(e))

    """
        Send a notification to a user

        Envoie une notification à un utilisateur
    """
    def notify(self):
        try:
            query = NotificationModel.Notif(title=self.title, text=self.text, link=self.link, priority=self.priority, is_read=self.is_read, icon=self.icon, icon_color=self.icon_color, user=self.user)

            db.session.add(query)
            db.session.commit()
            logger.info('Notification ' + query.title + ' added successfully')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Notify error : ' + str(e))
            raise NotifException(str(e))

    """
        Mark as read all notification

        Marque comme lu les notification
    """
    def mark_read(self):
        try:
            query = NotificationModel.Notif.query.filter_by(user=self.user, is_read=0).all()

            for fetch in query:
                fetch.is_read = 1
                db.session.add(fetch)
                db.session.commit()
            logger.info('Notification mark as read successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Mark read error : ' + str(e))
            raise NotifException(str(e))

    """
        Delete a notification

        Supprime une notification
    """
    def delete(self):
        try:
            query = NotificationModel.Notif.query.filter_by(id=self.id, user=self.user).first()

            db.session.delete(query)
            db.session.commit()
            logger.info('Delete notification successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Delete Notif error : ' + str(e))
            raise NotifException(str(e))
