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
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required
from onyx.decorators import admin_required
from onyx.api.exceptions import *
from onyx.api.machine import *
from onyxbabel import gettext

machine = Machine()

@api.route('machine')
@admin_required
@login_required
def get_machine():
    """
    @api {get} /machine Request Machines Information
    @apiName getMachine
    @apiGroup Machine
    @apiPermission authenticated

    @apiSuccess (200) {Object[]} machines List of Machines
    @apiSuccess (200) {Number} machines.id Id of Machines
    @apiSuccess (200) {String} machines.house House of Machines
    @apiSuccess (200) {String} machines.name Name of Machines
    @apiSuccess (200) {String} machines.room Room of Machines
    @apiSuccess (200) {String} machines.host Host of Machines

    @apiError MachineNotFound No Machine Found

    """
    return machine.get()

@api.route('machine/add', methods=['POST'])
@admin_required
@login_required
def add_machine():
    """
    @api {post} /machine/add Add Machine
    @apiName addMachine
    @apiGroup Machine
    @apiPermission authenticated

    @apiParam {String} house House of Machine
    @apiParam {String} name Name of Machine
    @apiParam {String} room Room of Machine
    @apiParam {String} host Host of Machine

    @apiSuccess (200) redirect Redirect to Option

    @apiError AlreadyExist This Machine already Exist

    """
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
    """
    @api {delete} /machine/delete Delete Machine
    @apiName deleteMachine
    @apiGroup Machine
    @apiPermission authenticated

    @apiParam {Number} id Id of Machine

    @apiSuccess (200) delete Machine Deleted

    @apiError MachineNotFound No Machine Found

    """
    try:
        machine.id = id
        return machine.delete()
    except MachineException:
        return machine.delete()
