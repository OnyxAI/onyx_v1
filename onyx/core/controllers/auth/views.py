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
from onyx.api.assets import Json
from os.path import exists
from onyx.api.exceptions import *
import os
import onyx
from onyx.api.user import *
import hashlib

json = Json()
auth = Blueprint('auth', __name__, url_prefix='/auth/' , template_folder=str(onyx.__path__[0])+'/templates')
user = User()

@login_manager.user_loader
def load_user(id):
    db.session.rollback()
    return UsersModel.User.query.get(int(id))

#Hello Home route
@auth.route('hello')
def hello():
    return render_template('account/hello.html',next=request.args.get('next'))

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
            if register == 0:
                flash(gettext('Passwords are not same !' ), 'error')
                return redirect(url_for('auth.register'))
            elif register == 1:
                flash(gettext('Account Added !') , 'success')
                return redirect(url_for('auth.hello'))
        except UserException:
            flash(gettext('A Account with this informations already exist !') , 'error')
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
            if login == 0:
                flash(gettext('Incorrect email or password !'), 'error')
                return redirect(url_for('auth.login'))
            else:
                flash(gettext('You are now connected'), 'success')
                return redirect(request.args.get('next') or url_for('core.index'))
        except UserException:
            flash(gettext('An error has occured !'), 'error')
            return redirect(url_for('auth.hello'))

#Logout
@auth.route('logout')
@login_required
def logout():
    try:
        user.logout()
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
    json.json = users
    return render_template('account/manage.html', id=json.decode())

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
        json.json = manage_user
        user_decoded = json.decode()
        return render_template('account/change.html', username=user_decoded['username'],email=user_decoded['email'])
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
                user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
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
                user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()

            change = user.change_user()
            if change == 0:
                flash(gettext('Passwords are not same !' ), 'error')
                return redirect(url_for('auth.change_account'))
            flash(gettext('Account changed successfully' ), 'success')
            return redirect(url_for('auth.change_account'))
        except UserException:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for('auth.account_manage'))
