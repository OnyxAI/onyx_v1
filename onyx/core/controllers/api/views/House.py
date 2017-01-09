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
from onyx.api.house import *
from onyxbabel import gettext

house = House()

@api.route('house')
@admin_required
@login_required
def get_house():
    return house.get()

@api.route('house/add', methods=['POST'])
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
        return house.add()
    except Exception:
		return house.add()


@api.route('house/delete/<int:id>')
@admin_required
@login_required
def delete_house(id):
    try:
        house.id = id
        return house.delete()
    except Exception:
        return house.delete()
