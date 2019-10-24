# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.extensions import db
from onyx.core.models import *
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.api.kernel import Kernel
from onyx.util.log import getLogger
from passlib.hash import sha256_crypt
import git, onyx


logger = getLogger('Install')
json = Json()
kernel = Kernel()

"""
    Make the Onyx installation done

    Classe qui fait l'installation d'Onyx
"""
class Install:

    def __init__(self):
        self.password = None
        self.username = None
        self.email = None

    """
        Create the admin account

        Permet de créer le compte administrateur
    """
    def set(self):
        try:
            hashpass = sha256_crypt.hash(self.password.encode('utf-8'))
            user = UsersModel.User(admin=1, username=self.username, password=hashpass, email=self.email, tutorial=0, background_color='#efefef', color='indigo darken-1')
            db.session.add(user)
            db.session.commit()

            self.init_db()

            kernel.train(kernel.set())

            logger.info('Successfully Installation')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Installation error : ' + str(e))
            raise InstallException(str(e))

    """
        initialize the navbar for this user

        Initialise la barre de navigateur pour cet utilisateur
    """
    def init_db(self):
        try:
            user = UsersModel.User.query.filter_by(username=self.username).first()
            json.path = onyx.__path__[0] + "/data/user/navbar.json"
            navbar = json.decode_path()

            for key in navbar:
                query = NavbarModel.Navbar(user=user.id, fa=key['fa'], url=key['url'], pourcentage=key['pourcentage'], tooltip=key['tooltip'])
                db.session.add(query)
                db.session.commit()

            logger.info('Navbar initialized for user : ' + user.username)

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Navbar initialisation error : ' + str(e))
            raise NavbarException(str(e))


    """
        Download all Onyx data from github repo

        Téléchargement des données d'Onyx via github
    """
    def get_data(self):
        try:
            git.Repo.clone_from('https://github.com/OnyxProject/onyx-data', onyx.__path__[0] + "/data/")

            logger.info('Successfully get Data')
        except Exception as e:
            logger.error('Get Data error : ' + str(e))
            raise DataException(str(e))

    """
        Update of Onyx Data

        Mise à jour des données d'Onyx
    """
    def update_data(self):
        try:
            repo = git.cmd.Git(onyx.__path__[0] + "/data/")
            repo.pull()

            kernel.train(kernel.set())

            logger.info('Updating data successfully')
        except Exception as e:
            logger.error('Updating data error : ' + str(e))
            raise DataException(str(e))
