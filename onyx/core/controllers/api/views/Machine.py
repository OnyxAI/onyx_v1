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
from flask import request, Response
from onyx.decorators import api_required
from onyx.api.exceptions import MachineException
from onyx.api.machine import Machine
from onyx.api.assets import Json

machine = Machine()
json = Json()

@api.route('machine')
@api_required
def get_machine():
    try:
        return Response(machine.get(), mimetype='application/json')
    except MachineException:
        return Response(json.encore({"status": "error"}), mimetype='application/json')

@api.route('machine/add', methods=['POST'])
@api_required
def add_machine():
    try:
        machine.name = request.form['name']
        machine.house = request.form['house']
        machine.room = request.form['room']
        machine.host = request.form['host']
        return Response(machine.add(), mimetype='application/json')
    except MachineException:
        return Response(json.encore({"status": "error"}), mimetype='application/json')


@api.route('machine/delete/<int:_id>')
@api_required
def delete_machine(_id):
    try:
        machine.id = _id
        return Response(machine.delete(), mimetype='application/json')
    except MachineException:
        return Response(json.encore({"status": "error"}), mimetype='application/json')
