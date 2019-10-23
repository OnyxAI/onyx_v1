# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
https://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask_login import logout_user, login_user, current_user
from flask import current_app as app
from onyx.core.models import *
from onyx.skills.core import *
from onyx.extensions import db, login_manager
from onyx.api.assets import Json
from onyx.api.navbar import *
from onyx.api.exceptions import *
from onyx.api.events import *
from onyx.util.log import getLogger
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import hashlib
import onyx

event = Event()
navbars = Navbar()
logger = getLogger('User')
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
        self.tutorial = 0
        self.background_color = '#efefef'
        self.color = 'indigo darken-1'

    def get(self):
        try:
            query = UsersModel.User.query.all()
            users = []
            for fetch in query:
                user = {}
                user['id'] = fetch.id
                user['admin'] = fetch.admin
                user['username'] = fetch.username
                user['color'] = fetch.color
                user['background_color'] = fetch.background_color
                user['password'] = fetch.password
                user['email'] = fetch.email
                user['tutorial'] = fetch.tutorial
                users.append(user)

            logger.info('Getting users data successfully')

            return json.encode(users)
        except Exception as e:
            logger.error('Getting users data error : ' + str(e))
            raise GetException(str(e))
            

    def get_user(self):
        try:
            query = UsersModel.User.query.filter_by(id=self.id).first()
            user = {}

            user['id'] = query.id
            user['admin'] = query.admin
            user['username'] = query.username
            user['color'] = query.color
            user['background_color'] = query.background_color
            user['password'] = query.password
            user['email'] = query.email
            user['tutorial'] = query.tutorial

            logger.info('Getting user data successfully')

            return json.encode(user)
        except Exception as e:
            logger.error('Getting user data error : ' + str(e))
            raise GetException(str(e))
            


    def add(self):
        try:
            db.session.rollback()
            if self.password == self.verifpassword:
                hashpass = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
                user = UsersModel.User(admin=0, username=self.username, password=hashpass, email=self.email, tutorial=self.tutorial, background_color=self.background_color, color=self.color)

                db.session.add(user)
                db.session.commit()
                init = self.init_navbar()
                logger.info('User registered : ' + self.username)
                return json.encode({"status":"success"})
            else:
                logger.error('Not same password Error')
                return json.encode({"status":"error", "message": "Not same password"})
        except Exception as e:
            db.session.rollback()
            logger.error('Error in register : ' + str(e))
            raise UserException(str(e))
            

    def init_navbar(self):
        try:
            user = UsersModel.User.query.filter_by(username=self.username).first()

            json.path = onyx.__path__[0] + "/data/user/navbar.json"

            navbar = json.decode_path()

            for key in navbar:
                query = NavbarModel.Navbar(user=user.id,fa=key['fa'],url=key['url'],pourcentage=key['pourcentage'],tooltip=key['tooltip'])
                db.session.add(query)
                db.session.commit()

            all_skills = get_raw_name(app.config['SKILL_FOLDER'])

            for skill in all_skills:
                folder = skill
                navbars.folder = folder
                navbars.username = self.username
                navbars.set_plugin_navbar_user()

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error("User Navbar Init Error : " + str(e))
            raise NavbarException(str(e))
            

    def login(self):
        try:
            password = self.password.encode('utf-8')
            registered_user = UsersModel.User.query.filter_by(email=self.email,password=hashlib.sha1(password).hexdigest()).first()
            if registered_user is None:
                logger.error("Wrong informations")
                return json.encode({"status":"error", "message": "Wrong Informations"})

            access_token = create_access_token(identity = registered_user.as_dict())
            refresh_token = create_refresh_token(identity = registered_user.as_dict())

            registered_user.authenticated = True
            login_user(registered_user)

            event.code = "user_connected"
            event.template = "user == " + str(registered_user.id)
            event.new()

            logger.info("User Connected : " + registered_user.username)

            return json.encode({"status":"success", "access_token": access_token, "refresh_token": refresh_token})
        except Exception as e:
            logger.error("User Connected Error : " + str(e))
            raise UserException(str(e))
            

    def logout_client(self):
        try:
            login_manager.login_view = 'auth.hello'
            logout_user()

            logger.info('User logout successfully')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('User logout error : ' + str(e))
            raise UserException(str(e))

    def logout_access(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel.RevokedToken(jti = jti)
            revoked_token.add()
            return json.encode({'message': 'Access token has been revoked'})
        except:
            return json.encode({'message': 'Something went wrong'}), 500

    def logout_refresh(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel.RevokedToken(jti = jti)
            revoked_token.add()
            return json.encode({'message': 'Refresh token has been revoked'})
        except:
            return json.encode({'message': 'Something went wrong'}), 500

    def delete(self):
        try:
            id_delete = self.id

            query = UsersModel.User.query.filter_by(id=id_delete).first()

            db.session.delete(query)
            db.session.commit()

            deleteCalendar = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.user.endswith(id_delete))
            for fetch in deleteCalendar:
                deleteEvent = CalendarModel.Calendar.query.filter_by(id=fetch.id).first()
                db.session.delete(deleteEvent)
                db.session.commit()

            deleteNavbar = NavbarModel.Navbar.query.filter(NavbarModel.Navbar.user.endswith(id_delete))
            for fetch in deleteNavbar:
                deleteNavbarRow = NavbarModel.Navbar.query.filter_by(id=fetch.id).first()
                db.session.delete(deleteNavbarRow)
                db.session.commit()

            logger.info('Delete ' + query.username + ' successfully')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Error delete user : ' + str(e))
            raise UserException(str(e))

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
                return json.encode({"status":"error", "message": "Password not match"})

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('User data changed error : ' + str(e))
            raise UserException(str(e))

    def finish_tutorial(self):
        try:
            query = UsersModel.User.query.filter_by(id=self.id).first()

            query.tutorial = 1

            db.session.add(query)
            db.session.commit()

            logger.info('User tutorial changed successfully')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error("User Tutorial Error : " + str(e))
            raise UserException(str(e))

    def get_avatar(self):
        try:
            user = UsersModel.User.query.filter_by(id=current_user.id).first()
            email = str(user.email)
            size = 60
            url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?s=" +str(size)
            return url
        except Exception as e:
            url = "https://www.gravatar.com/avatar?s=60"
            return url

    def get_avatar_id(self):
        try:
            user = UsersModel.User.query.filter_by(id=self.id).first()
            email = str(user.email)
            size = 60
            url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?s=" +str(size)
            return url
        except Exception as e:
            url = "https://www.gravatar.com/avatar?s=60"
            return url
