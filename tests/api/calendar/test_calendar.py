# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.api.calendar import Calendar
from onyx.core.models import *
import json
import pytest

calendar = Calendar()

@pytest.mark.usefixtures('db', 'user_test_a')
class Test_Calendar:

    def test_add_event(self, user_test_a):
        calendar.id = user_test_a.id
        calendar.title = 'Party'
        calendar.notes = 'With Maria'
        calendar.lieu = 'Park'
        calendar.start = '2017-05-29 20:00:00'
        calendar.start = '2017-05-29 22:00:00'
        calendar.color = '#0071c5'

        result = json.loads(calendar.add())

        assert result['status'] == 'success'

    def test_get_event(self, db, user_test_a):
        get_event = CalendarModel.Calendar(title='Party', idAccount=user_test_a.id)
        db.session.add(get_event)
        db.session.commit()

        calendar.id = user_test_a.id
        result = json.loads(calendar.get())

        assert result[0]['title'] == 'Party'
