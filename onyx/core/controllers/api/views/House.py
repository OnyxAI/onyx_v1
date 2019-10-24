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
from onyx.api.exceptions import HouseException
from onyx.api.house import House
from onyx.api.assets import Json

json = Json()
house = House()

@api.route('house')
@api_required
def get_house():
    try:
        return Response(house.get(), mimetype='application/json')
    except HouseException:
        return Response(json.encode({"status": "error"}), mimetype='application/json')


@api.route('house/add', methods=['POST'])
@api_required
def add_house():
    try:
        house.name = request.form['name']
        house.address = request.form['address']
        house.city = request.form['city']
        house.postal = request.form['postal']
        house.country = request.form['country']
        house.latitude = request.form['latitude']
        house.longitude = request.form['longitude']

        return Response(house.add(), mimetype='application/json')
    except HouseException:
        return Response(json.encode({"status": "error"}), mimetype='application/json')


@api.route('house/delete/<int:_id>')
@api_required
def delete_house(_id):
    try:
        house.id = _id

        return Response(house.delete(), mimetype='application/json')
    except HouseException:
        return Response(json.encode({"status": "error"}), mimetype='application/json')
