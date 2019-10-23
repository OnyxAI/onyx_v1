# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import core
from flask import render_template, request, redirect, url_for
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.api.transport import Ratp

json = Json()
ratp = Ratp()

@core.route('transport')
def transport():
    return render_template('transport/index.html')

#RER
@core.route('transport/rer', methods=['GET', 'POST'])
def rers():
    if request.method == 'GET':
        return render_template('transport/ratp/rer/index.html')
    elif request.method == 'POST':
        return redirect('transport/rer/' + request.form['rerline'])

@core.route('transport/rer/<string:name>', methods=['GET', 'POST'])
def rer(name):
    if request.method == 'GET':
        try:
            return render_template('transport/ratp/rer/'+name+'.html')
        except TransportException:
            return render_template('transport/ratp/rer/index.html')
    elif request.method == 'POST':
        ratp.line = name
        ratp.station = request.form['rerstation']
        ratp.direction = request.form['rerdirection']
        json.url = ratp.get_rer_schedule()
        result = json.decode_url()
        try:
            return render_template('transport/ratp/rer/result.html', result=result)
        except TransportException:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for('core.transport'))


#METRO
@core.route('transport/metro', methods=['GET', 'POST'])
def metros():
    if request.method == 'GET':
        return render_template('transport/ratp/metro/index.html')
    elif request.method == 'POST':
        return redirect('transport/metro/' + request.form['metroline'])



@core.route('transport/metro/<string:name>', methods=['GET', 'POST'])
def metro(name):
    if request.method == 'GET':
        try:
            return render_template('transport/ratp/metro/' + name + '.html')
        except TransportException:
            return render_template('transport/ratp/metro/index.html')
    elif request.method == 'POST':
        ratp.line = name
        ratp.station = request.form['metrostation']
        ratp.direction = request.form['metrodirection']
        json.url = ratp.get_metro_schedule()
        result = json.decode_url()
        try:
            return render_template('transport/ratp/metro/result.html', result=result)
        except TransportException:
            flash(gettext('An error has occured !') , 'error')
            return redirect(url_for('core.transport'))
