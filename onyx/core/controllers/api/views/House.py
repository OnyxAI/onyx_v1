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
from onyx.api.exceptions import *
from onyx.decorators import admin_required
from onyx.api.house import *
from onyxbabel import gettext

house = House()
"""
    @api {get} /house Request Houses Information
    @apiName getHouse
    @apiGroup House
    @apiPermission authenticated

    @apiSuccess (200) {Object[]} houses List of House
    @apiSuccess (200) {Number} houses.id Id of House
    @apiSuccess (200) {String} houses.name Name of House
    @apiSuccess (200) {String} houses.address Address of House
    @apiSuccess (200) {String} houses.city City of House
    @apiSuccess (200) {String} houses.country Country of House
    @apiSuccess (200) {String} houses.latitude Latitude of House
    @apiSuccess (200) {String} houses.longitude Longitude of House

    @apiError HouseNotFound No House Found

"""
@api.route('house')
@login_required
def get_house():
    return house.get()

"""
    @api {post} /house/add Add House
    @apiName addHouse
    @apiGroup House
    @apiPermission authenticated

    @apiParam {String} name Name of House
    @apiParam {String} address Address of House
    @apiParam {String} city City of House
    @apiParam {String} country Country of House
    @apiParam {String} latitude Latitude of House
    @apiParam {String} longitude Longitude of House

    @apiSuccess (200) redirect Redirect to Option

    @apiError AlreadyExist This House already Exist

"""
@api.route('house/add', methods=['POST'])
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
    except HouseException:
        return house.add()

"""
    @api {delete} /house/delete Delete House
    @apiName deleteHouse
    @apiGroup House
    @apiPermission authenticated

    @apiParam {Number} id Id of House

    @apiSuccess (200) delete House Deleted

    @apiError HouseNotFound No House Found

"""
@api.route('house/delete/<int:id>')
@login_required
def delete_house(id):
    try:
        house.id = id
        return house.delete()
    except HouseException:
        return house.delete()
