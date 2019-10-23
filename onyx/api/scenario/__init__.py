# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from flask import current_app as app
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.exceptions import *
from onyx.api.assets import Json
from onyx.util.log import getLogger
from onyx.config import get_config
import onyx

json = Json()
logger = getLogger('Scenario')

config = get_config('onyx')

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
        try:
            query = ScenarioModel.Scenario.query.filter(ScenarioModel.Scenario.user.endswith(self.user))
            
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
        except Exception as e:
            logger.error('Getting Scenario error : ' + str(e))
            raise ScenarioException(str(e))


    def add(self):
        try:
            query = ScenarioModel.Scenario(name=self.name, template=self.template, active=1, event=self.event, action=self.action, action_param=self.action_param, user=self.user)

            db.session.add(query)
            db.session.commit()

            return json.encode({"status": "success"})
        except Exception as e:
            logger.error('Adding Scenario error : ' + str(e))
            raise ScenarioException(str(e))


    def delete(self):
        try:
            query = ScenarioModel.Scenario.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()

            return json.encode({"status": "success"})
        except Exception as e:
            logger.error('Adding Scenario error : ' + str(e))
            raise ScenarioException(str(e))

    def delete_plugin(self):
        try:
            self.delete_plugin_action()
            logger.info('Plugin Scenario object deleted with success')

            return json.encode({"status": "success"})
        except Exception as e:
            logger.error('Plugin Scenario delete error : ' + str(e))
            raise ScenarioException(str(e))


    def delete_plugin_action(self):
        try:
            json.path = app.config['SKILL_FOLDER'] + self.plugin_name + "/data/actions/" + config.get('Base', 'lang') + ".json"
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
            return json.encode({"status": "success"})
        except Exception as e:
            logger.error('Deleting scenario plugin error : ' + str(e))
            raise ScenarioException(str(e))
