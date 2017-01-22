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
from onyx.api.exceptions import *
from onyx.api.assets import Json
from flask_login import current_user
import onyx, os
import logging

json = Json()
logger = logging.getLogger()

class Scenario:

    def __init__(self):
        self.id = None
        self.template = None
        self.name = None
        self.house = None
        self.user = None
        self.event = None
        self.action = None
        self.action_param = None
        self.plugin_name = None

    def get_all(self):
        query = ScenarioModel.Scenario.query.filter(ScenarioModel.Scenario.user.endswith(current_user.id))
        scenarios = []

        for key in query:
            e = {}
            e['id'] = key.id
            e['name'] = key.name
            e['template'] = key.template
            e['active'] = key.active
            e['event'] = key.event
            e['action'] = key.action
            e['action_param'] = key.action_param
            e['user'] = key.user
            scenarios.append(e)

        return json.encode(scenarios)


    def add(self):
        query = ScenarioModel.Scenario(name=self.name, template=self.template, active=1, event=self.event, action=self.action, action_param=self.action_param, user=self.user)

        db.session.add(query)
        db.session.commit()


    def delete(self):
        query = ScenarioModel.Scenario.query.filter_by(id=self.id).first()

        db.session.delete(query)
        db.session.commit()

    def delete_plugin(self):
        try:
            self.delete_plugin_action()
            logger.info('Plugin Scenario object deleted with success')
        except Exception as e:
            logger.error('Plugin Scenario delete error : ' + str(e))


    def delete_plugin_action(self):
        json.path = onyx.__path__[0] + "/plugins/" + self.plugin_name + "/data/actions.json"
        data = json.decode_path()
        user = UsersModel.User.query.all()
        for key in user:
            for plugin in data:
                try:
                    query = ScenarioModel.Scenario.query.filter_by(user=key.id,action=plugin['url']).first()

                    db.session.delete(query)
                    db.session.commit()
                except:
                    pass
