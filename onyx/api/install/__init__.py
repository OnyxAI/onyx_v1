# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyxbabel import gettext as _
from flask.ext.login import login_user, current_user, LoginManager
from onyx.extensions import db, login_manager
from onyx.core.models import *
from onyx.api.install import *
from onyx.api.assets import Json
import git
from git import Repo
import pip
import onyx
import os
import hashlib

json = Json()

class Install:

    def __init__(self):
        self.password = None
        self.username = None
        self.email = None


    def set(self):
        try:
            hashpass = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
            user = UsersModel.User(admin=1, username=self.username, password=hashpass, email=self.email)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            init = self.init_db()
            print(init)
            return json.encode({"status":"success"})
        except:
            raise Exception("An error has occured")
            return json.encode({"status":"error"})

    def init_db(self):
        try:
            user = UsersModel.User.query.filter_by(username=self.username).first()
            json.path = onyx.__path__[0] + "/data/user/navbar.json"
            navbar = json.decode_path()
            for key in navbar:
                query = NavbarModel.Navbar(idAccount=user.id,fa=key['fa'],url=key['url'],pourcentage=key['pourcentage'],tooltip=key['tooltip'])
                db.session.add(query)
                db.session.commit()
            return 'Init Done'
        except:
            return 'Init Error'

    def get_data(self):
        Repo.clone_from('https://github.com/OnyxProject/Onyx-Data', onyx.__path__[0] + "/data/")
        print('Done')


    def update_data(self):
        repo = git.cmd.Git(onyx.__path__[0] + "/data/")
        repo.pull()
        print('Done')
