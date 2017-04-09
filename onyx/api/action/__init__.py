# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import importlib, os, onyx, logging
from flask import current_app as app, g
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.config import get_config

logger = logging.getLogger()
json = Json()
config = get_config('onyx')

"""
    This class handles the possible actions of Onyx and is used by the scenario system

    Cette classe s'occupe de gérer les actions possible d'Onyx et est couplé avec le système de scénario
"""
class Action:

    def __init__(self):
        self.id = None
        self.app = app
        self.url = None
        self.param = None

    """
        This function makes it possible to get in the data folder and in each plugin all possible actions by Onyx, it stores them in a variable that it returns,
        All depending on the language of the user

        Cette fonction permet de récupérer dans le dossier data ainsi que dans chaque plugin toutes les actions possible par Onyx, elle les stocke dans une variable qu'elle renvoie,
        le tout en fonction de la langue de l'utilisateur
    """
    def get(self):

        try:
            """
                The language of the user is retrieved via the configuration file and the information about the available actions is retrieved

                On récupère la langue de l'utilisateur via le fichier de configuration et on récupère les informations concernant les actions disponible
            """
            lang = config.get('Base', 'lang')

            try:
                json.lang = lang
                json.data_name = "actions"
                data = json.decode_data()
            except:
                json.lang = "en-US"
                json.data_name = "actions"
                data = json.decode_data()


            """
                We retrieve for each plugin its actions available according to the language

                On récupère pour chaque plugin ses actions disponible en fonction de la langue
            """
            plugins = [d for d in os.listdir(onyx.__path__[0] + "/plugins/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/plugins/", d))]
            for plugin in plugins:
                try:
                    try:
                        json.path = onyx.__path__[0] + "/plugins/" + plugin + "/data/actions/" + lang + ".json"
                        data += json.decode_path()
                    except:
                        json.path = onyx.__path__[0] + "/plugins/" + plugin + "/data/actions/en-US.json"
                        data += json.decode_path()
                except Exception as e:
                    logger.error('Error get plugins : ' + str(e))

            """
                We return the data variable which contains all the actions

                On retourne la variable data qui contient toutes les actions
            """
            return json.encode(data)
        except Exception as e:
            logger.error('Getting action error : ' + str(e))
            raise GetException(str(e))


    """
        This function makes it possible, from the code of the action, to execute the action

        Cette fonction permet à partir du code de l'action d'éxecuter l'action
    """
    def start(self):
        function = getattr(importlib.import_module(self.app.view_functions[self.url].__module__), self.app.view_functions[self.url].__name__)
        try:
            execute = function()
        except TypeError:
            execute = function(self.param)
