# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import os
import sys
try:
    import Onyx
    sys.path.append(str(Onyx.__path__[0]))
except:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from flask import Flask, render_template, redirect, url_for
from onyx.extensions import (db, mail, login_manager, babel, cache)
from flask_login import current_user
from onyx.config import get_config
from onyx.plugins import plugin
from onyx.api.assets import Json
from onyx.api.server import *
from flask_turbolinks import turbolinks
server = Server()

json = Json()

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

server.create_config_file()
from onyx.flask_config import ProdConfig, Config


#Log
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

__all__ = ('create_app','blueprints_fabrics', 'get_blueprints', 'get_blueprint_name', 'error_pages')

def create_app(config=ProdConfig, app_name='onyx', blueprints=None):

    app = Flask(app_name,
        static_folder = 'static',
        template_folder = 'templates'
    )

    app.config.from_pyfile('../local.cfg', silent=True)
    if config:
        app.config.from_object(config)

    extensions_fabrics(app)
    set_log()
    gvars(app)

    with app.app_context():
        db.create_all()

    return app

def set_bot():
    kernel = ChatBot("Onyx",
        storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.TimeLogicAdapter",
            "chatterbot.logic.BestMatch"
        ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        output_format="text",
        database= onyx.__path__[0] + "/data/sentences/database.db"
    )

    kernel.set_trainer(ChatterBotCorpusTrainer)

    kernel.train(
        onyx.__path__[0] + "/data/sentences/" + config.get('Base', 'lang') + "/"
    )

    return kernel

def init_plugin(app):
    with app.app_context():
        for module in plugin:
            try:
                module.init(app)
            except:
                module.init()

def get_blueprint_name(app):
    return 'core'


def get_blueprints(app):
    from onyx.core.controllers.base import core
    from onyx.core.actions import action
    from onyx.core.controllers.auth import auth
    from onyx.core.controllers.api import api
    from onyx.core.widgets import widgets
    from onyx.core.controllers.install import install
    BLUEPRINTS = [core, auth, api, action, widgets,]
    for module in plugin:
        try:
            BLUEPRINTS.append(module.get_blueprint())
        except:
            print('No Blueprint for module : ' + module.get_name())

    for blueprint in BLUEPRINTS:
        @blueprint.before_request
        def check_install():
            if app.config['INSTALL'] == False:
                return redirect(url_for('install.index'))

    BLUEPRINTS.append(install)
    return BLUEPRINTS


def set_log():
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.INFO)
    logger.addHandler(steam_handler)



def blueprints_fabrics(app, blueprints):
    """Configure blueprints in views."""
    try:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
    except:
        app.register_blueprint(blueprints)

def extensions_fabrics(app):
    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)

def gvars(app):
    @app.before_request
    def get_vars():
        try:
            server.user = current_user
            server.get_vars()
        except Exception as e:
            logger.error('Get vars error : ' + str(e))
            raise ServerException(str(e))
            return json.encode({"status":"error"})

    @app.context_processor
    def utility_processor():
        def get_params(url):
            function = getattr(importlib.import_module(app.view_functions[url].__module__), app.view_functions[url].__name__)
            execute = function()
            json.json = execute
            return json.decode()
        return dict(get_params=get_params)

    @app.context_processor
    def utility_processor():
        def get_variable(p,variable):
            v = str(variable.encode('ascii'))
            return p[v]
        return dict(get_variable=get_variable)

    @app.context_processor
    def ButtonColor():
        try:
            buttonColor = current_user.buttonColor
        except:
            buttonColor = ""
        return dict(buttonColor=str(buttonColor))

    @app.context_processor
    def gravatar():
        def urlPicAvatar(id):
            user.id = id
            return user.get_avatar_id()
        return dict(urlPicAvatar=urlPicAvatar)

    @app.context_processor
    def inject_user():
        try:
            return {'user': g.user}
        except AttributeError:
            return {'user': None}

    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
            db.session.remove()
        db.session.remove()

    try:
        @babel.localeselector
        def get_locale():
            raw_lang = config.get('Base', 'lang')
            if raw_lang:
                lang = raw_lang.split('-')
                if lang[0] in Config.ACCEPT_LANGUAGES:
                    return lang[0]
                else:
                    return Config.BABEL_DEFAULT_LOCALE
            else:
                return 'fr'
    except AssertionError:
        pass

def error_pages(app , name):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("404.html", blueprint=name), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html" , blueprint=name), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("404.html", blueprint=name), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("404html", blueprint=name), 500
