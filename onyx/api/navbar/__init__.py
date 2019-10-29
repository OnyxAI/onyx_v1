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
from flask import current_app as app
from onyx.core.models import *
from onyxbabel import gettext
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.extensions import db
import onyx
from onyx.util.log import getLogger

logger = getLogger('Navbar')
json = Json()

"""
    This class handles the user's navbar

    Cette classe gère la barre de navigation de l'utilisateur
"""
class Navbar:

    def __init__(self):
        self.user = None
        self.id = None
        self.fa = None
        self.url = None
        self.pourcentage = None
        self.tooltip = None
        self.new = None
        self.last = None
        self.folder = None
        self.username = None

    """
        Get the navbar of a user

        Récupère la barre de navigation d'un utilisateur
    """
    def get(self):
        try:
            navbar = []
            query = NavbarModel.Navbar.query.filter_by(user=self.user).limit(11)
            for key in query:
                e = {}
                e['id'] = key.id
                e['fa'] = key.fa
                e['url'] = key.url
                e['pourcentage'] = key.pourcentage
                e['tooltip'] =  gettext(key.tooltip)
                navbar.append(e)

            return json.encode(navbar)
        except Exception as e:
            raise NavbarException(str(e))

    """
        Get the list of available app

        Récupère la liste des applications disponible
    """
    def get_list(self):
        try:
            list = []
            query = NavbarModel.Navbar.query.filter(NavbarModel.Navbar.user.endswith(self.user))
            for fetch in query:
                e = {}
                e['id'] = fetch.id
                e['fa'] = fetch.fa
                e['url'] = fetch.url
                e['tooltip'] = fetch.tooltip
                list.append(e)
            return json.encode(list)
        except Exception as e:
            raise NavbarException(str(e))

    """
        Change an element of the navbar

        Modifie un élément de la navbar
    """
    def set_navbar(self):
        try:
            last_nav = NavbarModel.Navbar.query.filter_by(id=self.last).first()
            new_nav = NavbarModel.Navbar.query.filter_by(id=self.new).first()

            new_url = new_nav.url
            new_tooltip = new_nav.tooltip
            new_fa = new_nav.fa

            last_url = last_nav.url
            last_tooltip = last_nav.tooltip
            last_fa = last_nav.fa

            #Update New
            last_nav.url = new_url
            last_nav.tooltip = new_tooltip
            last_nav.fa = new_fa

            #Update Last
            new_nav.url = last_url
            new_nav.tooltip = last_tooltip
            new_nav.fa = last_fa

            #Update
            db.session.add(last_nav)
            db.session.commit()
            db.session.add(new_nav)
            db.session.commit()

            logger.info('Navbar updated successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Navbar update error : ' + str(e))
            raise NavbarException(str(e))

    """
        Allows the installation of a plugin to initialize the navbar

        Permet des l'installation d'un plugin d'initialisé sa navbar
    """
    def set_plugin_navbar(self):
        try:
            json.path = app.config['SKILL_FOLDER'] + self.folder + "/package.json"
            data = json.decode_path()
            if data['navbar'] == 'True':
                json.path = app.config['SKILL_FOLDER'] + self.folder + "/navbar.json"
                data = json.decode_path()
                user = UsersModel.User.query.all()
                for key in user:
                    for nav in data:
                        query = NavbarModel.Navbar(user=key.id,fa=nav['fa'],url=nav['url'],tooltip=nav['tooltip'])
                        db.session.add(query)
                        db.session.commit()
                logger.info('Navbar plugin set with success')
            else:
                logger.info('No navbar for : ' + data['name'])
        except Exception as e:
            logger.error('Navbar plugin set error : ' + str(e))
            raise NavbarException(str(e))

    """
        Allows the installation of a plugin to initialize the navbar for a user

        Permet des l'installation d'un plugin d'initialisé sa navbar pour un utilisateur
    """
    def set_plugin_navbar_user(self):
        try:
            json.path = app.config['SKILL_FOLDER'] + self.folder + "/package.json"
            data = json.decode_path()
            if data['navbar'] == 'True':
                json.path = app.config['SKILL_FOLDER'] + self.folder + "/navbar.json"
                data_skill = json.decode_path()
                user = UsersModel.User.query.filter_by(username=self.username).first()
                for nav in data_skill:
                    query = NavbarModel.Navbar(user=user.id,fa=nav['fa'],url=nav['url'],tooltip=nav['tooltip'])
                    db.session.add(query)
                    db.session.commit()
                logger.info('Navbar set with success for ' + data['name'])
            else:
                logger.info('No navbar for : ' + data['name'])
        except Exception as e:
            logger.error('Navbar use set error : ' + str(e))
            raise NavbarException(str(e))

    """
        Removes applications from the navbar when a plugin is uninstalled

        Supprime les applications de la navbar quand un plugin est désinstallé
    """
    def delete_plugin_navbar(self):
        try:
            json.path = app.config['SKILL_FOLDER'] + self.folder + "/navbar.json"
            data = json.decode_path()
            user = UsersModel.User.query.all()
            for key in user:
                for nav in data:
                    query = NavbarModel.Navbar.query.filter_by(user=key.id,tooltip=nav['tooltip']).first()
                    query.url = None
                    query.tooltip = "Undefined"
                    query.fa = None
                    db.session.add(query)
                    db.session.commit()
                    
            logger.info('Navbar object deleted with success')
        except Exception as e:
            logger.error('Navbar delete error : ' + str(e))
            raise NavbarException(str(e))
