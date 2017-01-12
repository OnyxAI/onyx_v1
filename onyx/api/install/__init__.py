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
from onyx.api.exceptions import *
import git, pip, onyx, os, hashlib, logging
from git import Repo

logger = logging.getLogger()
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
            self.init_db()
            logger.info('Successfully Installation')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Installation error : ' + str(e))
            raise InstallException(str(e))
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
            logger.info('Navbar initialized for user : ' + user.username)
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Navbar initialisation error : ' + str(e))
            raise NavbarException(str(e))
            return json.encode({"status":"error"})

    def get_data(self):
        try:
            Repo.clone_from('https://github.com/OnyxProject/Onyx-Data', onyx.__path__[0] + "/data/")
            logger.info('Successfully get Data')
        except Exception as e:
            logger.error('Get Data error : ' + str(e))
            raise DataException(str(e))


    def update_data(self):
        try:
            repo = git.cmd.Git(onyx.__path__[0] + "/data/")
            repo.pull()
            logger.info('Updating data successfully')
        except Exception as e:
            logger.error('Updating data error : ' + str(e))
            raise DataException(str(e))
