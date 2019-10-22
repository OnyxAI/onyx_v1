# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.hello'

from onyxbabel import Babel
babel = Babel()

from flask_migrate import Migrate
migrate = Migrate()

from flask_cache import Cache
cache = Cache()
