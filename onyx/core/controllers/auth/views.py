# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from passlib.hash import sha256_crypt
from flask_login import login_required, current_user
from flask import request, render_template, g, flash, redirect, url_for, session
from flask_jwt_extended import get_jti
from onyxbabel import gettext
from onyx.extensions import login_manager, db
from onyx.decorators import admin_required
from onyx.api.assets import Json
from onyx.api.events import Event
from onyx.api.token import Token
from onyx.api.user import User
from onyx.util import getLogger
from onyx.api.exceptions import *
from . import auth

logger = getLogger('Auth')
event = Event()
token_api = Token()
json = Json()
user = User()

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))

#Hello Home route
@auth.route('hello')
def hello():
    return render_template('account/hello.html', next=request.args.get('next'))

#Hello Home route
@auth.route('finish_tutorial')
@login_required
def finish_tutorial():
    try:
        user.id = current_user.id

        return user.finish_tutorial()
    except:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.index'))

#Register
@auth.route('register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('account/register.html')
    elif request.method == 'POST':
        try:
            user.password = request.form['password']
            user.verifpassword = request.form['verifpassword']
            user.username = request.form['username']
            user.email = request.form['email']

            register = user.add()

            if json.decode(register).get('status') == 'error':
                flash(gettext('Passwords are not same !' ), 'error')
                return redirect(url_for('auth.register'))
            elif json.decode(register).get('status') == 'success':
                flash(gettext('Account Added !') , 'success')
                return redirect(url_for('auth.hello'))
        except UserException:
            flash(gettext('A Account with this informations already exist !'), 'error')
            return redirect(url_for('auth.hello'))


#Login
@auth.route('login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')
    elif request.method == 'POST':
        try:
            user.email = request.form['email']
            user.password = request.form['password']
            login = user.login()
            session["token"] = json.decode(login).get('access_token')

            if json.decode(login).get('status') == 'error':
                flash(gettext('Incorrect email or password !'), 'error')
                return redirect(url_for('auth.login'))
            else:
                flash(gettext('You are now connected'), 'success')
                return redirect(request.args.get('next') or url_for('core.index'))
        except UserException:
            flash(gettext('An error has occured !'), 'error')
            return redirect(url_for('auth.hello'))

#Add Token
@auth.route('add_token',methods=['GET','POST'])
@admin_required
@login_required
def add_token():
    if request.method == 'POST':
        try:
            token_api.name = request.form['name']
            
            result = token_api.add()

            if json.decode(result).get('status') == 'error':
                flash(gettext('An error has occured !'), 'error')
                return redirect(url_for('core.options'))
            else:
                flash(gettext('Token Added'), 'success')
                return redirect(url_for('core.options'))
        except TokenException:
            flash(gettext('An error has occured !'), 'error')
            return redirect(url_for('core.options'))


#Delete Token
@auth.route('delete_token/<id>', methods=['GET','POST'])
@admin_required
@login_required
def delete_token(id):
    if request.method == 'GET':
        try:
            token_api.id = id
            token_api.token = get_jti(session['token'])
            
            result = token_api.delete()

            if json.decode(result).get('status') == 'error':
                flash(gettext('An error has occured !'), 'error')
                return redirect(url_for('core.options'))
            else:
                flash(gettext('Token Deleted'), 'success')
                return redirect(url_for('core.options'))
        except TokenException:
            flash(gettext('An error has occured !'), 'error')
            return redirect(url_for('core.options'))

#Logout
@auth.route('logout')
@login_required
def logout():
    try:
        user.logout_client()

        logger.info('User Logout successfully')

        flash(gettext('You are now log out' ), 'info')
        return redirect(url_for('auth.hello'))
    except UserException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('auth.hello'))

#Manage Accounts (Admin)
@auth.route('account/manage')
@admin_required
@login_required
def account_manage():
    users = user.get()

    return render_template('account/manage.html', id=json.decode(users))

#Delete Accounts (Admin)
@auth.route('account/delete/<id_delete>')
@admin_required
@login_required
def delete_account(id_delete):
    try:
        user.id = id_delete
        user.delete()

        flash(gettext('Account deleted !') , 'success')
        return redirect(url_for('auth.account_manage'))
    except UserException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('auth.hello'))

#Manage User (Admin)
@auth.route('account/manage/<id>', methods=['GET','POST'])
@admin_required
@login_required
def account_manage_id(id):
    if request.method == 'GET':
        user.id = id
        manage_user = user.get_user()

        user_decoded = json.decode(manage_user)
        return render_template('account/change.html', username=user_decoded['username'], email=user_decoded['email'])
    elif request.method == 'POST':
        try:
            user.id = id
            manage_user = user.get_user()
            json.json = manage_user
            user_decoded = json.decode()
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
                user.password = sha256_crypt.hash(request.form['password'].encode('utf-8'))
                

            user.manage_user()

            flash(gettext('Account changed !') , 'success')
            return redirect(url_for('auth.account_manage'))
        except UserException:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for('auth.account_manage'))

#Modify Account
@auth.route('account/change' , methods=['GET','POST'])
@login_required
def change_account():
    if request.method == 'GET':
        return render_template('account/manage_account.html')
    elif request.method == 'POST':
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
                user.password = sha256_crypt.hash(request.form['password'].encode('utf-8'))

            change = user.change_user()
            
            if json.decode(change).get('status') == 'error':
                flash(gettext('Passwords are not same !' ), 'error')
                return redirect(url_for('auth.change_account'))
            flash(gettext('Account changed successfully' ), 'success')
            return redirect(url_for('auth.change_account'))
        except UserException:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for('auth.account_manage'))
