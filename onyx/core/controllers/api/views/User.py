# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask.ext.login import LoginManager, login_required
from flask import request, render_template, Blueprint, current_app, g, flash, redirect
from onyxbabel import gettext
from onyx.extensions import login_manager, db
from onyx.decorators import admin_required
from os.path import exists
import os
import onyx
from onyx.api.user import *
from onyx.api.account import *
import hashlib
from .. import api

user = User()

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))

#Register
@api.route('users')
def get_users():
    """
    @api {get} /users Get User
    @apiName users
    @apiGroup User
    @apiPermission authenticated
    @apiPermission admin

    @apiSuccess (200) {Object[]} user Get All User Information

    """
    users = user.get()
    return users



@api.route('user',methods=['POST'])
def register():
    """
    @api {post} /user Register a User
    @apiName registerUser
    @apiGroup User

    @apiParam {String} username User Name
    @apiParam {String} password User Password
    @apiParam {String} verifpassword User Verification Password
    @apiParam {String} email User Email

    @apiSuccess (200) redirect Redirect to Hello

    @apiError AlreadyExist This User already Exist

    """
    try:
        user.password = request.form['password']
        user.verifpassword = request.form['verifpassword']
        user.username = request.form['username']
        user.email = request.form['email']
        register = user.add()
        if register == 0:
            return register
        elif register == 1:
            return register
    except Exception:
        return register


#Login
@api.route('user/login',methods=['POST'])
def login():
    if request.method == 'POST':
        """
        @api {post} /user/login Login User
        @apiName registerUser
        @apiGroup User

        @apiParam {String} username User Name
        @apiParam {String} password User Password
        @apiParam {String} verifpassword User Verification Password
        @apiParam {String} email User Email

        @apiSuccess (200) redirect Redirect to Hello

        @apiError AlreadyExist This User already Exist

        """
        try:
            user.email = request.form['email']
            user.password = request.form['password']
            login = user.login()
            if login == 0:
                return login
            else:
                return login
        except Exception:
            return login

#Logout
@api.route('user/logout')
@login_required
def logout():
    return user.logout()



#Delete Accounts (Admin)
@api.route('user/delete/<id_delete>')
@admin_required
@login_required
def delete_account(id_delete):
    """
    @api {get} /user/delete/:id Delete User
    @apiName deleteAccount
    @apiGroup User
    @apiPermission authenticated
    @apiPermission admin

    @apiSuccess (200) redirect Redirect To Manage Account

    """
    user.id = id_delete
    return user.delete()

#Manage User (Admin)
@api.route('user/manage/<id>', methods=['GET','POST'])
@admin_required
@login_required
def account_manage_id(id):
    if request.method == 'GET':
        """
        @api {get} /user/manage/:id Get User
        @apiName manageUserGet
        @apiGroup User
        @apiPermission authenticated
        @apiPermission admin

        @apiSuccess (200) {Object[]} user Get User Information

        """
        user.id = id
        manage_user = user.get_user()
        return manage_user

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
        try:
            user.id = id
            manage_user = user.get_user()
            user_decoded = decodeJSON.decode(manage_user)
            if not request.form['username']:
                user.username = user_decoded['username']
            else:
                user.username = request.form['username']
            if not request.form['email']:
                user.email = user_decoded['email']
            else:
                user.email = request.form['email']
            if not request.form['password']:
                user.password = user_decoded['password']
            else:
                user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
            return user.manage_user()
        except Exception:
            return user.manage_user()

#Modify Account
@api.route('user/change' , methods=['POST'])
@login_required
def change_account():
    if request.method == 'POST':
        """
        @api {post} /user/change Update Account
        @apiName changeAccount
        @apiGroup User
        @apiPermission authenticated

        @apiParam {String} username User Name
        @apiParam {String} password User Password
        @apiParam {String} email User Email

        @apiSuccess (200) redirect Redirect To Change Account

        """
        try:
            user.id = current_user.id
            user.lastpassword = request.form['lastpassword']
            if not request.form['username']:
                user.username = current_user.username
            else:
                user.username = request.form['username']
            if not request.form['email']:
                user.email = current_user.email
            else:
                user.email = request.form['email']
            if not request.form['password']:
                user.password = current_user.password
            else:
                user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()

            change = user.change_user()
            if change == 0:
                return change
            return change
        except Exception:
            return change
