# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
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
from flask import g, current_app as app
from onyx.skills.core import *
from onyx.util import getLogger
import onyx
import os

json = Json()
logger = getLogger('Widgets')

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
        try:
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
        except Exception as e:
            logger.error('Getting widget error : ' + str(e))
            raise GetException(str(e))

    def get_list(self):
        try:
            try:
                json.path = app.config['DATA_FOLDER'] + "widgets/" + g.lang + ".json"
            except:
                json.path = app.config['DATA_FOLDER'] + "widgets/en-US.json"
            data = json.decode_path()

            all_skills = get_raw_name(app.config['SKILL_FOLDER'])
            for skill in all_skills:
                try:
                    try:
                        json.path = app.config['SKILL_FOLDER'] + skill + "/data/widgets/" + g.lang + ".json"
                        data += json.decode_path()
                    except:
                        logger.info('No widget for : ' + skill)
                except Exception as e:
                    logger.error('Error get plugins : ' + str(e))

            return json.encode(data)
        except Exception as e:
            logger.error('Getting widget list error : ' + str(e))
            raise GetException(str(e))

    def add(self):
        try:
            query = WidgetsModel.Widget(user=current_user.id, url=self.url, color=self.color, name=self.name, see_more=self.see_more)

            db.session.add(query)
            db.session.commit()
        except Exception as e:
            logger.error('Adding Widget error : ' + str(e))
            raise WidgetException(str(e))

    def delete(self):
        try:
            query = WidgetsModel.Widget.query.filter_by(user=current_user.id,id=self.id).first()

            db.session.delete(query)
            db.session.commit()
        except Exception as e:
            logger.error('Deleting Widget error : ' + str(e))
            raise WidgetException(str(e))

    def delete_plugin(self):
        try:
            json.path = app.config['SKILL_FOLDER'] + self.plugin_name + "/data/widgets.json"
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
            raise WidgetException(str(e))
