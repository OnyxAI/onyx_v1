"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask import render_template, request

from onyx.api.transport import *

@core.route('transport')
def transport():
    return render_template('transport/index.html')

#RER
@core.route('transport/rer', methods=['GET', 'POST'])
def rers():
    if request.method == 'GET':
        return render_template('transport/ratp/rer/index.html')
    elif request.method == 'POST':
        return redirect('transport/rer/'+request.form['rerline'])

@core.route('transport/rer/<string:name>', methods=['GET', 'POST'])
def rer(name):
    if request.method == 'GET':
        """
        @api {get} /transport/rer/:string Get Rer Info
        @apiName getRer
        @apiGroup Transport | RER
        @apiPermission authenticated 

        @apiSuccess (200) {String} name Name of RER
        @apiSuccess (200) {select} station Get Station
        @apiSuccess (200) {select} direction Get Direction

        @apiError NoName No Rer Name Found
        """
        try:
            return render_template('transport/ratp/rer/'+name+'.html')
        except:
            return render_template('transport/ratp/rer/index.html')
    elif request.method == 'POST':
        """
        @api {post} /transport/rer/:string Get Rer Schedule Info
        @apiName serRer
        @apiGroup Transport | RER
        @apiPermission authenticated 

        @apiParam {String} name Name of RER
        @apiParam {select} station Station
        @apiParam {select} direction Direction

        @apiSuccess (200) {json} result Schedule Result
        @apiSuccess (200) {String} result.horaire Rer Schedule
        @apiSuccess (200) {String} result.name Rer Station

        @apiError NoExist No Schedule Exist for This Rer
        
        """
        return setRer(name)

#METRO
@core.route('transport/metro', methods=['GET', 'POST'])
def metros():
    if request.method == 'GET':
        return render_template('transport/ratp/metro/index.html')
    elif request.method == 'POST':
        return redirect('transport/metro/'+request.form['metroline']) 



@core.route('transport/metro/<string:name>', methods=['GET', 'POST'])
def metro(name):
    if request.method == 'GET':
        """
        @api {get} /transport/metro/:string Get Metro Info
        @apiName getMetro
        @apiGroup Transport | Metro
        @apiPermission authenticated 

        @apiSuccess (200) {String} name Name of Metro
        @apiSuccess (200) {select} station Get Station
        @apiSuccess (200) {select} direction Get Direction

        @apiError NoName No Metro Name Found
        """
        try:
            return render_template('transport/ratp/metro/'+name+'.html')
        except:
            return render_template('transport/ratp/metro/index.html')
    elif request.method == 'POST':
        """
        @api {post} /transport/metro/:string Get Metro Schedule Info
        @apiName serMetro
        @apiGroup Transport | Metro
        @apiPermission authenticated 

        @apiParam {String} name Name of Metro
        @apiParam {select} station Station
        @apiParam {select} direction Direction

        @apiSuccess (200) {json} result Schedule Result
        @apiSuccess (200) {String} result.horaire Metro Schedule
        @apiSuccess (200) {String} result.name Metro Station

        @apiError NoExist No Schedule Exist for This Station
        
        """
        return setMetro(name)
