# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.api.notification import Notification
from onyx.core.models import *
import json
import pytest

notif = Notification()

@pytest.mark.usefixtures('db', 'user_test_a')
class Test_Notification:

    def test_notify(self, user_test_a):
        notif.user = user_test_a.id
        notif.title = 'User Connected'
        notif.text = 'A user was connected in Onyx'
        notif.link = None
        notif.priority = 0
        notif.is_read = 0
        notif.ison = 'fa-users'
        notif.icon_bolor = 'blue'

        result = json.loads(notif.notify())

        assert result['status'] == 'success'

    def test_get_all_notification(self, db, user_test_a):
        get_notif = NotificationModel.Notif(title='User Connected', text='A user was connected in Onyx', link=None, priority=0, is_read=0, icon='fa-users', icon_color='blue', user=user_test_a.id)
        db.session.add(get_notif)
        db.session.commit()

        notif.user = user_test_a.id
        result = json.loads(notif.get_all())

        assert result[0]['title'] == 'User Connected'

    def test_get_notification(self, db, user_test_a):
        get_notif = NotificationModel.Notif(title='User Connected', text='A user was connected in Onyx', link=None, priority=0, is_read=1, icon='fa-users', icon_color='blue', user=user_test_a.id)
        db.session.add(get_notif)
        db.session.commit()

        notif.user = user_test_a.id
        result = json.loads(notif.get())

        assert result == []

    def test_mark_read(self, db, user_test_a):
        get_notif = NotificationModel.Notif(title='User Connected', text='A user was connected in Onyx', link=None, priority=0, is_read=0, icon='fa-users', icon_color='blue', user=user_test_a.id)
        db.session.add(get_notif)
        db.session.commit()

        notif.user = user_test_a.id
        mark = json.loads(notif.mark_read())
        result = json.loads(notif.get_all())

        assert result[0]['is_read'] == 1
        assert mark['status'] == 'success'

    def test_delete_notif(self, db, user_test_a):
        get_notif = NotificationModel.Notif(title='User Connected', text='A user was connected in Onyx', link=None, priority=0, is_read=0, icon='fa-users', icon_color='blue', user=user_test_a.id)
        db.session.add(get_notif)
        db.session.commit()

        notif.id = get_notif.id
        notif.user = user_test_a.id
        result = json.loads(notif.delete())

        assert result['status'] == 'success'
