"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager, login_required
from flask import request, render_template, Blueprint, current_app, g
from onyx.extensions import login_manager, db
from onyx.decorators import admin_required
from os.path import exists
import os

from onyx.api.user import *
from onyx.api.account import *

try:
    import Onyx 
    auth = Blueprint('auth', __name__, url_prefix='/auth/' , template_folder=str(Onyx.__path__[0])+'/onyx/templates')
except:
    auth = Blueprint('auth', __name__, url_prefix='/auth/' , template_folder=os.path.dirname(os.path.dirname(__file__))+'/onyx/templates')
    

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))
  

#Hello Home route
@auth.route('hello')
def hello():
    return render_template('account/hello.html')
  
#Register
@auth.route('register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('account/register.html')
    elif request.method == 'POST':
        """
        @api {post} /register Register a User
        @apiName registerUser
        @apiGroup User

        @apiParam {String} username User Name
        @apiParam {String} password User Password
        @apiParam {String} verifpassword User Verification Password
        @apiParam {String} email User Email

        @apiSuccess (200) redirect Redirect to Hello

        @apiError AlreadyExist This User already Exist
        
        """
        return registerUser()

#Login
@auth.route('login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')
    elif request.method == 'POST':
        """
        @api {post} /login Login User
        @apiName registerUser
        @apiGroup User

        @apiParam {String} username User Name
        @apiParam {String} password User Password
        @apiParam {String} verifpassword User Verification Password
        @apiParam {String} email User Email

        @apiSuccess (200) redirect Redirect to Hello

        @apiError AlreadyExist This User already Exist
        
        """
        return loginUser()

#Logout
@auth.route('logout')
@login_required
def logout():
    return logoutUser()
    
#Manage Accounts (Admin)
@auth.route('account/manage')
@admin_required
@login_required
def account_manage():
    """
    @api {get} /account/manage Manage User
    @apiName manageAccount
    @apiGroup User
    @apiPermission authenticated
    @apiPermission admin

    @apiSuccess (200) {Object[]} user Get All User Information
        
    """
    return manageAccount()
        
#Delete Accounts (Admin)
@auth.route('account/delete/<id_delete>')
@admin_required
@login_required
def delete_account(id_delete):
    """
    @api {get} /account/delete/:id Delete User
    @apiName deleteAccount
    @apiGroup User
    @apiPermission authenticated
    @apiPermission admin

    @apiSuccess (200) redirect Redirect To Manage Account
        
    """
    return deleteAccount(id_delete)
			
#Manage User (Admin)
@auth.route('account/manage/<id>', methods=['GET','POST'])
@admin_required
@login_required
def account_manage_id(id):
    if request.method == 'GET':
        """
        @api {get} /account/manage/:id Manage User
        @apiName manageUserGet
        @apiGroup User
        @apiPermission authenticated
        @apiPermission admin

        @apiSuccess (200) {Object[]} user Get User Information
        
        """
        user = UsersModel.User.query.filter_by(id=id).first()
        return render_template('account/change.html', username=user.username,email=user.email)
    elif request.method == 'POST':
        """
        @api {post} /account/delete/:id Update User
        @apiName manageUser
        @apiGroup User
        @apiPermission authenticated
        @apiPermission admin

        @apiParam {String} username User Name
        @apiParam {String} password User Password
        @apiParam {String} email User Email

        @apiSuccess (200) redirect Redirect To Manage Account
        
        """
        return manageUser(id)

#Modify Account
@auth.route('account/change' , methods=['GET','POST'])
@login_required
def change_account():
    if request.method == 'GET':
        """
        @api {get} /account/change Manage Account
        @apiName manageAccountGet
        @apiGroup User
        @apiPermission admin

        @apiSuccess (200) {Object[]} user Get User Information
        
        """
        bdd = UsersModel.User.query.filter_by(username=current_user.username).first()
        buttonColor = bdd.buttonColor
        return render_template('account/manage_account.html' ,buttonColor=str(buttonColor) )
    elif request.method == 'POST':
        """
        @api {post} /account/change Update Account
        @apiName changeAccount
        @apiGroup User
        @apiPermission authenticated

        @apiParam {String} username User Name
        @apiParam {String} password User Password
        @apiParam {String} email User Email

        @apiSuccess (200) redirect Redirect To Change Account
        
        """
        return changeAccount()


