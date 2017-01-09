# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.core.models import *
from onyx.extensions import db

def delete_scenario_db(id):
	query = ScenarioModel.Scenario.query.filter_by(id=id).first()

	db.session.delete(query)
	db.session.commit()
