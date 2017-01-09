# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask_login import current_user
from time import strftime
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.assets import Json

json = Json()

class Calendar:

    def __init__(self):
        self.id = 0
        self.title = 'Undefined'
        self.notes = 'Undefined'
        self.lieu = 'Home'
        self.color = '#0071c5'
        self.startdate = strftime("%Y-%m-%d  %H:%M:%S")
        self.enddate = strftime("%Y-%m-%d  %H:%M:%S")

    def add(self):

        try:
            query = CalendarModel.Calendar(idAccount=current_user.id,\
                                           title=self.title,\
                                           notes=self.notes,\
                                           lieu=self.lieu,\
                                           start=self.startdate,\
                                           end=self.enddate,\
                                           color=self.color)
            db.session.add(query)
            db.session.commit()
            return json.encode({"status":"success"})
        except:
            return json.encode({"status":"error"})

    def get(self):
        query = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(current_user.id))
        events = []

        for fetch in query:
    		e = {}
    		e['id'] = fetch.id
    		e['title'] = fetch.title
    		e['notes'] = fetch.notes
    		e['lieu'] = fetch.lieu
    		e['start'] = fetch.start
    		e['end'] = fetch.end
    		e['color'] = fetch.color
    		events.append(e)

        return json.encode(events)



    def update_date(self):
        try:
            query = CalendarModel.Calendar.query.filter_by(id=self.id,idAccount=current_user.id).first()
            query.start = self.startdate
            query.end = self.enddate

            db.session.add(query)
            db.session.commit()

            return json.encode({'status':'success'})
        except:
            return json.encode({'status':'error'})

    def delete(self):
        try:
            delete = CalendarModel.Calendar.query.filter_by(id=self.id,idAccount=current_user.id).first()

            db.session.delete(delete)
            db.session.commit()
            return json.encode({'status':'success'})
        except:
            return json.encode({'status':'error'})

    def update_event(self):
        try:
            update = CalendarModel.Calendar.query.filter_by(id=self.id,idAccount=current_user.id).first()
            update.title = self.title
            update.notes = self.notes
            update.lieu = self.lieu
            update.color = self.color

            db.session.add(update)
            db.session.commit()
            return json.encode({'status':'success'})
        except:
            return json.encode({'status':'error'})
