# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask_mail import Mail
mail = Mail()

from onyx_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()
try:
	login_manager.login_view = 'auth.hello'
except:
	login_manager.login_view = 'install.installer'

from onyxbabel import Babel , Domain
babel = Babel()

from flask_migrate import Migrate
migrate = Migrate()

from flask_cache import Cache
cache = Cache()

from celery import Celery
celery = Celery()
