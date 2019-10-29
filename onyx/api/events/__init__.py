# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.assets import Json
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.action import *
from flask import g, current_app as app
import os, onyx
from onyx.api.exceptions import *
from onyx.config import get_config
from onyx.util.log import getLogger

logger = getLogger('Event')
action = Action()
json = Json()
config = get_config('onyx')

"""
    This class allows to manage the event part of Onyx

    Cette classe permet de gérer la partie évenement d'Onyx
"""
class Event:

    def init(self):
        self.app = app
        self.id = None
        self.code = None
        self.template = ""

    """
        Allows to retrieve all possible events in Onyx and plugins

        Permet de récupérer tous les évenements possible dans Onyx et dans les plugins
    """
    def get(self):
        try:
            """
                The language of the user is retrieved via the configuration file and the information about the available events is retrieved

                On récupère la langue de l'utilisateur via le fichier de configuration et on récupère les informations concernant les évenements disponible
            """
            try:
                lang = config.get('Base', 'lang')
            except:
                json.lang = "en-US"

            json.data_name = "events"
            data = json.decode_data()

            """
                We retrieve for each plugin its events available according to the language

                On récupère pour chaque plugin ses évenements disponible en fonction de la langue
            """
            all_skills = get_raw_name(app.config['SKILL_FOLDER'])
            for skill in all_skills:
                try:
                    try:
                        json.path = app.config['SKILL_FOLDER'] + skill + "/data/events/" + lang + ".json"
                        data += json.decode_path()
                    except:
                        logger.info('No events for : ' + skill)
                except Exception as e:
                    logger.error('Error get skills : ' + str(e))


            return json.encode(data)
        except Exception as e:
            logger.error('Error getting events : ' + str(e))

    """
        This function executes the corresponding action(s) according to the scenario

        Cette fonction execute la ou les action(s) correspondante(s) en fonction du scénario
    """
    def new(self):
        try:
            code = self.code
            query = ScenarioModel.Scenario.query.filter_by(event=code).all()

            for key in query:
                if self.template == key.template:
                    action.url = key.action
                    action.param = key.action_param
                    action.start()
        except Exception as e:
            logger.error('New event error : ' + str(e))
            raise EventException(str(e))
