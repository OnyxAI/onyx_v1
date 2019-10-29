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
from flask import  request, Response
from onyx.decorators import api_required
from onyx.api.geolocalisation import Geolocalisation
from onyx.api.assets import Json
from onyx.api.exceptions import *

geoloc = Geolocalisation()
json = Json()

@api.route('/geolocalisation', methods=['GET'])
@api_required
def geo():
    if request.method == 'GET':
        try:
            return Response(json.encode(geoloc.get_all()), mimetype='application/json')
        except WikiException:
            return Response(json.encode({"status": "error"}), mimetype='application/json')
