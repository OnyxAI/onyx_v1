# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import Blueprint, render_template, redirect, request, current_app, g, flash, url_for
from flask_login import login_required, logout_user
from onyxbabel import gettext as _
import os, onyx


core = Blueprint('core', __name__, url_prefix='/' , template_folder=onyx.__path__[0] + '/templates')


from .views import *
