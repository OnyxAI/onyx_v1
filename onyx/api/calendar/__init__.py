# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
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
from onyx.api.exceptions import *
from onyx.util.log import getLogger

logger = getLogger('Calendar')
json = Json()

"""
    This class allows to manage the Calendar and the Events in Onyx

    Cette classe permet de gérer le Calendrier et les Evenements dans Onyx
"""
class Calendar:

    def __init__(self):
        self.user = None
        self.id = None
        self.title = 'Undefined'
        self.notes = 'Undefined'
        self.lieu = 'Home'
        self.color = '#0071c5'
        self.startdate = strftime("%Y-%m-%d  %H:%M:%S")
        self.enddate = strftime("%Y-%m-%d  %H:%M:%S")

    """
        This function adds an event in the database according to the user

        Cette fonction ajoute un évenement dans la base de donné en fonction de l'utilisateur
    """
    def add(self):
        try:
            query = CalendarModel.Calendar(user=self.user,\
                                           title=self.title,\
                                           notes=self.notes,\
                                           lieu=self.lieu,\
                                           start=self.startdate,\
                                           end=self.enddate,\
                                           color=self.color)
            db.session.add(query)
            db.session.commit()
            logger.info('Event ' + self.title + ' added successfully')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Event added error : ' + str(e))
            raise CalendarException(str(e))

    """
        This function retrieves all the events of a given user

        Cette fonction récupère tous les évenements d'un utilisateur donné
    """
    def get(self):
        try:
            query = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.user.endswith(self.user)).all()
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
        except Exception as e:
            logger.error('Getting event error : ' + str(e))
            raise CalendarException(str(e))

    """
        This function allows you to retrieve all the events of the day of a user

        Cette fonction permet de récupérer tous les évenements du jour d'un utilisateur
    """
    def get_meet(self):
        try:
            query = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.start.like(strftime("%Y-%m-%d")+"%")).all()
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
        except Exception as e:
            logger.error('Getting meet error : ' + str(e))
            raise CalendarException(str(e))


    """
        This function updates the date of an event

        Cette fonction met a jour la date d'un évenement
    """
    def update_date(self):
        try:
            query = CalendarModel.Calendar.query.filter_by(id=self.id, user=self.user).first()
            query.start = self.startdate
            query.end = self.enddate

            db.session.add(query)
            db.session.commit()

            return json.encode({'status':'success'})
        except Exception as e:
            logger.error('Event update error : ' + str(e))
            raise CalendarException(str(e))

    """
        This function delete an event

        Cette fonction supprime un évenement
    """
    def delete(self):
        try:
            delete = CalendarModel.Calendar.query.filter_by(id=self.id,user=self.user).first()

            db.session.delete(delete)
            db.session.commit()

            return json.encode({'status':'success'})
        except:
            return json.encode({'status':'error'})

    """
        This function updates an event

        Cette fonction met a jour un évenement
    """
    def update_event(self):
        try:
            update = CalendarModel.Calendar.query.filter_by(id=self.id,user=self.user).first()
            update.title = self.title
            update.notes = self.notes
            update.lieu = self.lieu
            update.color = self.color

            db.session.add(update)
            db.session.commit()

            logger.info('Event ' + update.title + ' update')

            return json.encode({'status':'success'})
        except Exception as e:
            
            logger.error('Event update error : ' + str(e))
            raise CalendarException(str(e))
