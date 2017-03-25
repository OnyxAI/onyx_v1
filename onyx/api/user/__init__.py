# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask.ext.login import logout_user, login_user, current_user
from flask import request , render_template , redirect , url_for , flash
from onyxbabel import gettext
from onyx.core.models import *
from onyx.extensions import db, login_manager
from onyx.api.assets import Json
from onyx.api.navbar import *
from onyx.api.exceptions import *
from onyx.plugins import plugin
import hashlib
import onyx
import logging

navbars = Navbar()
logger = logging.getLogger()
json = Json()


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
            logger.info('Getting users data successfully')
            return json.encode(users)
        except Exception as e:
            logger.error('Getting users data error : ' + str(e))
            raise GetException(str(e))
            return json.encode({"status":"error"})

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
            logger.info('Getting user data successfully')
            return json.encode(user)
        except Exception as e:
            logger.error('Getting user data error : ' + str(e))
            raise GetException(str(e))
            return json.encode({"status":"error"})


    def add(self):
        try:
            db.session.rollback()
            if self.password == self.verifpassword:
                hashpass = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
                user = UsersModel.User(admin=0, username=self.username, password=hashpass, email=self.email)

                db.session.add(user)
                db.session.commit()
                init = self.init_navbar()
                logger.info('User registered : ' + self.username)
                return 1
            else:
                logger.error('No same password Error')
                return 0
        except Exception as e:
            db.session.rollback()
            logger.error('Error in register : ' + str(e))
            raise UserException(str(e))
            return json.encode({"status":"error"})

    def init_navbar(self):
        try:
            user = UsersModel.User.query.filter_by(username=self.username).first()
            json.path = onyx.__path__[0] + "/data/user/navbar.json"
            navbar = json.decode_path()
            for key in navbar:
                query = NavbarModel.Navbar(idAccount=user.id,fa=key['fa'],url=key['url'],pourcentage=key['pourcentage'],tooltip=key['tooltip'])
                db.session.add(query)
                db.session.commit()
            for module in plugin:
                folder = module.get_raw()
                navbars.folder = folder
                navbars.username = self.username
                navbars.set_plugin_navbar_user()
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error("User Navbar Init Error : " + str(e))
            raise NavbarException(str(e))
            return json.encode({"status":"error"})

    def login(self):
        try:
            password = self.password.encode('utf-8')
            registered_user = UsersModel.User.query.filter_by(email=self.email,password=hashlib.sha1(password).hexdigest()).first()
            if registered_user is None:
                logger.error("Wrong for : " + registered_user.username)
                return 0
            login_user(registered_user)
            registered_user.authenticated = True
            logger.info("User Connected : " + registered_user.username)
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error("User Connected Error : " + str(e))
            raise UserException(str(e))
            return json.encode({"status":"error"})

    def logout(self):
        try:
            login_manager.login_view = 'auth.hello'
            logout_user()
            logger.info('User logout successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('User logout error : ' + str(e))
            raise Exception('Error logout')
            return json.encode({"status":"error"})

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
            logger.info('Delete ' + query.username + ' successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Error delete user : ' + str(e))
            raise UserException(str(e))
            return json.encode({"status":"error"})

    def manage_user(self):
        try:
            query = UsersModel.User.query.filter_by(id=self.id).first()

            query.username = self.username
            query.password = self.password
            query.email = self.email

            db.session.add(query)
            db.session.commit()
            logger.info('Getting users successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Error getting users : ' + str(e))
            raise UserException(str(e))
            return json.encode({"status":"error"})

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
                logger.info('User data changed successfully')
                return json.encode({"status":"success"})
            else:
                return 0
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('User data changed error : ' + str(e))
            raise UserException(str(e))
            return json.encode({"status":"error"})

    def get_avatar(self):
        try:
            user = UsersModel.User.query.filter_by(id=current_user.id).first()
            email = str(user.email)
            default = "http://www.gravatar.com/avatar"
            size = 60
            url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?d=" + default + "&s=" +str(size)
            return url
        except Exception as e:
            url = "http://www.gravatar.com/avatar?s=60"
            return url

    def get_avatar_id(self):
        try:
            user = UsersModel.User.query.filter_by(id=self.id).first()
            email = str(user.email)
            default = "http://www.gravatar.com/avatar"
            size = 60
            url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?d=" + default + "&s=" +str(size)
            return url
        except Exception as e:
            url = "http://www.gravatar.com/avatar?s=60"
            return url
