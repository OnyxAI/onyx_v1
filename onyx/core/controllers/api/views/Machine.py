# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import api
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from onyx.decorators import admin_required
from onyx.api.exceptions import *
from onyx.api.machine import *
from onyxbabel import gettext

machine = Machine()

@api.route('machine')
@admin_required
@login_required
def get_machine():
    return machine.get()

@api.route('machine/add', methods=['POST'])
@admin_required
@login_required
def add_machine():
    try:
        machine.name = request.form['name']
        machine.house = request.form['house']
        machine.room = request.form['room']
        machine.host = request.form['host']
        return machine.add()
    except MachineException:
			return machine.add()


@api.route('machine/delete/<int:id>')
@admin_required
@login_required
def delete_machine(id):
    try:
        machine.id = id
        return machine.delete()
    except MachineException:
        return machine.delete()
