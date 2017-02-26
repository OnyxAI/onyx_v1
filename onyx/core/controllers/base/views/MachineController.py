# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import core
from flask import request, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from onyx.decorators import admin_required
from onyx.api.exceptions import *
from onyx.api.machine import *
from onyxbabel import gettext

machine = Machine()

@core.route('machine/add', methods=['POST'])
@admin_required
@login_required
def add_machine():
    try:
        machine.name = request.form['name']
        machine.house = request.form.get('house')
        machine.room = request.form.get('room')
        machine.host = request.form['host']
        machine.add()
        flash(gettext('Machine Add'), 'success')
        return redirect(url_for('core.options'))
    except MachineException:
			flash(gettext('An error has occured !'), 'error')
			return redirect(url_for('core.options'))


@core.route('machine/delete/<int:id>')
@admin_required
@login_required
def delete_machine(id):
    try:
        machine.id = id
        machine.delete()
        flash(gettext('Machine Deleted'), 'success')
        return redirect(url_for('core.options'))
    except MachineException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.options'))
