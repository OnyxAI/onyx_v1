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
from flask import request, session, Response
from flask_jwt_extended import decode_token, get_jwt_identity
from onyx.decorators import api_required
from onyx.api.exceptions import *
from onyx.api.notification import *
from onyx.api.assets import Json

notif = Notification()
json = Json()

@api.route('notification/all', methods=['GET'])
@api_required
def get_notif():
    if request.method == 'GET':
        try:
            try:
                current_user = decode_token(session['token'])['identity']
            except:	
                current_user = get_jwt_identity()

            notif.user = current_user['id']
            
            return Response(notif.get_all(), mimetype='application/json')
        except:
            return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('notification/unread', methods=['GET'])
@api_required
def get_unread_notif():
    if request.method == 'GET':
        try:
            try:
                current_user = decode_token(session['token'])['identity']
            except:	
                current_user = get_jwt_identity()

            notif.user = current_user['id']
            
            return Response(notif.get(), mimetype='application/json')
        except:
            return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('notification/mark_read', methods=['GET'])
@api_required
def mark_read():
    if request.method == 'GET':
        try:
            try:
                current_user = decode_token(session['token'])['identity']
            except:	
                current_user = get_jwt_identity()

            notif.user = current_user['id']
            
            return Response(notif.mark_read(), mimetype='application/json')
        except:
            return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('notification', methods=['POST'])
@api_required
def add_notif():
    if request.method == 'POST':
        try:
            try:
                current_user = decode_token(session['token'])['identity']
            except:	
                current_user = get_jwt_identity()

            notif.user = current_user['id']
            notif.title = request.form.get('title')
            notif.text = request.form.get('text')
            notif.priority = request.form.get('priority')
            notif.icon = request.form.get('icon')
            notif.icon_color = request.form.get('icon_color')

            return Response(notif.notify(), mimetype='application/json')
        except:
            return Response(json.encode({"status": "error"}), mimetype='application/json')


@api.route('notification/delete/<int:id>')
@api_required
def delete_notifications(id):
    try:
        try:
            current_user = decode_token(session['token'])['identity']
        except:	
            current_user = get_jwt_identity()

        notif.id = id
        notif.user = current_user['id']
        
        return Response(notif.delete(), mimetype='application/json')
    except NotifException:
        return Response(json.encode({"status": "error"}), mimetype='application/json')

