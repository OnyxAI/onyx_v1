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
from onyx.core.models import *
from onyxbabel import gettext
from onyx.api.assets import Json
from onyx.extensions import db
import onyx

json = Json()

class Navbar:

    def __init__(self):
        self.id = None
        self.fa = None
        self.url = None
        self.pourcentage = None
        self.tooltip = None
        self.new = None
        self.last = None
        self.folder = None
        self.username = None

    def get(self):
        try:
            navbar = []
            query = NavbarModel.Navbar.query.filter_by(idAccount=current_user.id).limit(11)
            for key in query:
                e = {}
                e['id'] = key.id
                e['fa'] = key.fa
                e['url'] = key.url
                e['pourcentage'] = key.pourcentage
                e['tooltip'] =  gettext(key.tooltip)
                navbar.append(e)

            return json.encode(navbar)
        except:
            return 0

    def get_list(self):
        try:
            list = []
            query = NavbarModel.Navbar.query.filter(NavbarModel.Navbar.idAccount.endswith(str(current_user.id)))
            for fetch in query:
                e = {}
                e['id'] = fetch.id
                e['fa'] = fetch.fa
                e['url'] = fetch.url
                e['tooltip'] = fetch.tooltip
                list.append(e)
            return json.encode(list)
        except:
            return 0

    def set_navbar(self):
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

        print('Done')
        return True

    def set_plugin_navbar(self):
        json.path = onyx.__path__[0] + "/plugins/" + self.folder + "/navbar.json"
        data = json.decode_path()
        user = UsersModel.User.query.all()
        for key in user:
            for nav in data:
                query = NavbarModel.Navbar(idAccount=key.id,fa=nav['fa'],url=nav['url'],tooltip=nav['tooltip'])
                db.session.add(query)
                db.session.commit()
        print('Set Done')

    def set_plugin_navbar_user(self):
        json.path = onyx.__path__[0] + "/plugins/" + self.folder + "/navbar.json"
        data = json.decode_path()
        user = UsersModel.User.query.filter_by(username=self.username).first()
        for nav in data:
            query = NavbarModel.Navbar(idAccount=user.id,fa=nav['fa'],url=nav['url'],tooltip=nav['tooltip'])
            db.session.add(query)
            db.session.commit()
        print('Set Done')

    def delete_plugin_navbar(self):
        json.path = onyx.__path__[0] + "/plugins/" + self.folder + "/navbar.json"
        data = json.decode_path()
        user = UsersModel.User.query.all()
        for key in user:
            for nav in data:
                query = NavbarModel.Navbar.query.filter_by(idAccount=key.id,tooltip=nav['tooltip']).first()
                query.url = None
                query.tooltip = "Undefined"
                query.fa = None
                db.session.add(query)
                db.session.commit()
        print('Delete Done')
