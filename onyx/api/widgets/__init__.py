# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.exceptions import *
from onyx.api.assets import Json
from flask_login import current_user
from onyxbabel import gettext
from onyx.extensions import db
from onyx.core.models import *
from flask import g
import logging
import onyx
import os

json = Json()
logger = logging.getLogger()

class Widgets:

    def __init__(self):
        self.id = None
        self.url = None
        self.user = None
        self.color = None
        self.name = None
        self.see_more = None
        self.plugin_name = None

    def get(self):
        query = WidgetsModel.Widget.query.filter_by(user=current_user.id).all()
        widgets = []

        for key in query:
            e = {}
            e['id'] = key.id
            e['user'] = key.user
            e['color'] = key.color
            e['url'] = key.url
            e['name'] = key.name
            e['see_more'] = key.see_more
            widgets.append(e)

        return json.encode(widgets)

    def get_list(self):
        try:
            json.path = onyx.__path__[0] + "/data/widgets/" + g.lang + ".json"
        except:
            json.path = onyx.__path__[0] + "/data/widgets/fr.json"
        data = json.decode_path()

        plugins = [d for d in os.listdir(onyx.__path__[0] + "/plugins/") if os.path.isdir(os.path.join(onyx.__path__[0] + "/plugins/", d))]
        for plugin in plugins:
            try:
                json.path = onyx.__path__[0] + "/plugins/" + plugin + "/data/widgets.json"
                data += json.decode_path()
            except:
                print('Error')

        return json.encode(data)

    def add(self):
        query = WidgetsModel.Widget(user=current_user.id, url=self.url, color=self.color, name=self.name, see_more=self.see_more)

        db.session.add(query)
        db.session.commit()

    def delete(self):
        query = WidgetsModel.Widget.query.filter_by(user=current_user.id,id=self.id).first()

        db.session.delete(query)
        db.session.commit()

    def delete_plugin(self):
        try:
            json.path = onyx.__path__[0] + "/plugins/" + self.plugin_name + "/data/widgets.json"
            data = json.decode_path()
            user = UsersModel.User.query.all()
            for key in user:
                for plugin in data:
                    query = WidgetsModel.Widget.query.filter_by(user=key.id,url=plugin['url']).first()

                    db.session.delete(query)
                    db.session.commit()
            logger.info('Plugin Widget object deleted with success')
        except Exception as e:
            logger.error('Plugin Widget delete error : ' + str(e))
