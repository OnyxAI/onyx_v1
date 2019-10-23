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
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required
from onyx.decorators import admin_required
from onyx.api.exceptions import *
from onyx.api.house import *
from onyxbabel import gettext

house = House()

@core.route('house/add', methods=['POST'])
@admin_required
@login_required
def add_house():
    try:
        house.name = request.form['name']
        house.address = request.form['address']
        house.city = request.form['city']
        house.postal = request.form['postal']
        house.country = request.form['country']
        house.latitude = request.form['latitude']
        house.longitude = request.form['longitude']
        house.add()

        flash(gettext('House Add'), 'success')
        return redirect(url_for('core.options'))
    except HouseException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.options'))


@core.route('house/delete/<int:id>')
@admin_required
@login_required
def delete_house(id):
    try:
        house.id = id
        house.delete()

        flash(gettext('House Deleted'), 'success')
        return redirect(url_for('core.options'))
    except HouseException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.options'))
