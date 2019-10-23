# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import api
from flask import request
from onyx.api.assets import Json
from onyx.decorators import admin_api_required, api_required
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token
from onyx.api.user import User
from onyx.api.exceptions import UserException, GetException

import hashlib

json = Json()
user = User()


#Register
@api.route('users')
@api_required
def get_users():
    try:
        users = user.get()
        return users
    except GetException:
        return json.encode({"status": "error"})

@api.route('get_access_token')
@jwt_refresh_token_required
def get_access_token():
    try:
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return json.encode({'access_token': access_token})
    except GetException:
        return json.encode({"status": "error"})

#Register
@api.route('user/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            user.password = request.form['password']
            user.verifpassword = request.form['verifpassword']
            user.username = request.form['username']
            user.email = request.form['email']

            register = user.add()
            
            return register
        except UserException:
            return json.encode({"status": "error"})


#Login
@api.route('user/login',methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            user.email = request.form['email']
            user.password = request.form['password']

            login = user.login()

            return login
        except UserException:
            return json.encode({"status": "error"})

#Logout Access
@api.route('user/logout_access')
@jwt_required
def logout_access():
    return user.logout_access()

#Logout Refresh
@api.route('user/logout_access')
@jwt_refresh_token_required
def logout_refresh():
    return user.logout_refresh()


#Delete Accounts (Admin)
@api.route('user/delete/<id_delete>')
@api_required
@admin_api_required
def delete_account(id_delete):
    try:
        user.id = id_delete
        return user.delete()
    except UserException:
        return json.encode({"status": "error"})

#Manage User (Admin)
@api.route('user/manage/<id>', methods=['GET','POST'])
@api_required
@admin_api_required
def account_manage_id(id):
    if request.method == 'GET':
        try:
            user.id = id
            manage_user = user.get_user()

            return manage_user
        except UserException:
            return json.encode({"status": "error"})
    elif request.method == 'POST':
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
        except UserException:
            return json.encode({"status": "error"})

#Modify Account
@api.route('user/change' , methods=['POST'])
@api_required
def change_account():
    if request.method == 'POST':
        try:
            current_user = get_jwt_identity()
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

            return change
        except UserException:
            return json.encode({"status": "error"})
