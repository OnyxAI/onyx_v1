"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager , login_user , login_required , current_user , login_user , logout_user
from flask import request , render_template , redirect , url_for , flash , session , Blueprint, current_app, g
from onyxbabel import gettext
from ..models import *
from ..extensions import db , login_manager


plugins = Blueprint('plugins', __name__, url_prefix='/plugins/', template_folder="templates")

from .controllers import *
from .models import *