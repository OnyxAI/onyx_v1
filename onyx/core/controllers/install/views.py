"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, request, current_app, g, flash, url_for
from flask.ext.login import login_required
from onyx.extensions import db
from onyx.core.models import *

from onyx.api.install import *

install = Blueprint('install', __name__, url_prefix='/', template_folder='templates')

@install.route('/' , methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('install/index.html')
    elif request.method == 'POST':
    	"""
		@api {post} /install Install Form
		@apiName setInstall
		@apiGroup Install

		@apiParam {String} username User Name
		@apiParam {String} password User Password
		@apiParam {String} email User Email

		@apiSuccess (200) redirect Redirect to Restart

		@apiError AlreadyExist This User already Exist
		
		"""
        return setInstall()
    
@install.route('finish')
@login_required
def finish():
    return render_template('install/finish.html')

