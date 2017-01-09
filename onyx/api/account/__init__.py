# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask.ext.login import logout_user, login_user
from flask import request , render_template , redirect , url_for , flash
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db, login_manager
from onyx.api.assets import decodeJSON
from onyx.api.navbar import *
from onyx.plugins import plugin
import hashlib
import json

class User:

    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.verifpassword = None
        self.lastpassword = None
        self.email = None
        self.admin = None

    def get(self):
        try:
            query = UsersModel.User.query.all()
            users = []
            for fetch in query:
                user = {}
                user['id'] = fetch.id
                user['admin'] = fetch.admin
                user['username'] = fetch.username
                user['lang'] = fetch.lang
                user['buttonColor'] = fetch.buttonColor
                user['password'] = fetch.password
                user['email'] = fetch.email
                users.append(user)

            return json.dumps(users)
        except:
            raise Exception('Error Get')
            return json.dumps({"status":"error"})

    def get_user(self):
        try:
            query = UsersModel.User.query.filter_by(id=self.id).first()
            user = {}

            user['id'] = query.id
            user['admin'] = query.admin
            user['username'] = query.username
            user['lang'] = query.lang
            user['buttonColor'] = query.buttonColor
            user['password'] = query.password
            user['email'] = query.email

            return json.dumps(user)
        except:
            raise Exception('Error Get User')
            return json.dumps({"status":"error"})


    def add(self):
        try:
            db.session.rollback()
            if self.password == self.verifpassword:
                hashpass = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
                user = UsersModel.User(admin=0, username=self.username, password=hashpass, email=self.email)

                db.session.add(user)
                db.session.commit()
                init = self.init_navbar()
                return 1
            else:
                return 0
        except:
            db.session.rollback()
            raise Exception('Error Register')
            return json.dumps({"status":"error"})

    def init_navbar(self):
        try:
            user = UsersModel.User.query.filter_by(username=self.username).first()
            navbar = decodeJSON.decode_navbar()
            for key in navbar:
                query = NavbarModel.Navbar(idAccount=user.id,fa=key['fa'],url=key['url'],pourcentage=key['pourcentage'],tooltip=key['tooltip'])
                db.session.add(query)
                db.session.commit()
            for module in plugin:
                folder = module.get_raw()
                set_plugin_navbar_user(folder,self.username)
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error Navbar')
            return json.dumps({"status":"error"})

    def login(self):
        try:
            password = self.password.encode('utf-8')
            registered_user = UsersModel.User.query.filter_by(email=self.email,password=hashlib.sha1(password).hexdigest()).first()
            if registered_user is None:
                return 0
            login_user(registered_user)
            registered_user.authenticated = True
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error login')
            return json.dumps({"status":"error"})

    def logout(self):
        try:
            login_manager.login_view = 'auth.hello'
            logout_user()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error logout')
            return json.dumps({"status":"error"})

    def delete(self):
        try:
            id_delete = self.id
            query = UsersModel.User.query.filter_by(id=id_delete).first()
            db.session.delete(query)
            db.session.commit()
            deleteCalendar = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(id_delete))
            for fetch in deleteCalendar:
                deleteEvent = CalendarModel.Calendar.query.filter_by(id=fetch.id).first()
                db.session.delete(deleteEvent)
                db.session.commit()
            deleteNavbar = NavbarModel.Navbar.query.filter(NavbarModel.Navbar.idAccount.endswith(id_delete))
            for fetch in deleteNavbar:
                deleteNavbarRow = NavbarModel.Navbar.query.filter_by(id=fetch.id).first()
                db.session.delete(deleteNavbarRow)
                db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error delete')
            return json.dumps({"status":"error"})

    def manage_user(self):
        try:
            query = UsersModel.User.query.filter_by(id=self.id).first()

            query.username = self.username
            query.password = self.password
            query.email = self.email

            db.session.add(query)
            db.session.commit()
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error manage')
            return json.dumps({"status":"error"})

    def change_user(self):
        try:
            query = UsersModel.User.query.filter_by(id=self.id).first()
            lastpassword = query.password

            if hashlib.sha1(self.lastpassword.encode('utf-8')).hexdigest() == lastpassword:

                query.username = self.username
                query.password = self.password
                query.email = self.email

                db.session.add(query)
                db.session.commit()
                return json.dumps({"status":"success"})
            else:
                return 0
            return json.dumps({"status":"success"})
        except:
            raise Exception('Error manage')
            return json.dumps({"status":"error"})
