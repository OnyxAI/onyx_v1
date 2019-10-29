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
from flask import request, session, Response
from onyx.api.skills import Skill
from onyx.api.assets import Json
from onyx.decorators import api_required
from onyx.api.exceptions import *


json = Json()
skill = Skill()

@api.route('skills')
@api_required
def skills():
	try:
		return Response(skill.get(), mimetype='application/json')
	except Exception as e:
		return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('skills/list')
@api_required
def skills_list():
	try:
		return Response(skill.get_list(), mimetype='application/json')
	except Exception as e:
		return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('skills/install/<string:name>')
@api_required
def install_skill(name):
	try:
		skill.name = name
		skill.url = request.args['url']

		return Response(skill.install(), mimetype='application/json')
	except Exception as e:
		return Response(json.encode({"status": "error"}), mimetype='application/json')


@api.route('skills/install_url', methods=['POST'])
@api_required
def install_skill_url():
	try:
		skill.name = request.form['name']
		skill.url = request.form['url']

		return Response(skill.install(), mimetype='application/json')
	except Exception as e:
		return Response(json.encode({"status": "error"}), mimetype='application/json')


@api.route('skills/uninstall/<string:name>')
@api_required
def uninstall_skill(name):
	try:
		skill.name = name

		return Response(skill.uninstall(), mimetype='application/json')
	except Exception as e:
		return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('skills/update/<string:name>')
@api_required
def update_skill(name):
	try:
		skill.name = name
		
		return Response(skill.update(), mimetype='application/json')
	except Exception as e:
		return Response(json.encode({"status": "error"}), mimetype='application/json')

