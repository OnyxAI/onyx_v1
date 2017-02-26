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
import aiml
from flask import Flask, render_template
from onyx.extensions import (db, mail, login_manager, babel, cache, celery)
from flask_login import current_user
from onyx.config import get_config
from onyx.api.server import *
from celery import Celery
from onyx.plugins import plugin

server = Server()

try:
    from onyx.flask_config import ProdConfig
except:
    server.create_config_file()
    from onyx.flask_config import ProdConfig

#Log
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


__all__ = ('create_app', 'create_celery','blueprints_fabrics', 'get_blueprints', 'get_blueprint_name', 'error_pages')

def create_app(config=ProdConfig, app_name='onyx', blueprints=None):

    app = Flask(app_name,
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
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
    kernel = aiml.Kernel()
    kernel.setPredicate('base_dir',onyx.__path__[0])
    kernel.bootstrap(learnFiles = onyx.__path__[0] + "/data/sentences/fr/std-startup.xml", commands = "load aiml b")
    return kernel

def init_plugin(app):
    with app.app_context():
        for module in plugin:
            try:
                module.init(app)
            except:
                module.init()

def get_blueprint_name(app):
    installConfig = get_config(app.config['INSTALL_FOLDER'])
    if installConfig.getboolean('Install', 'install'):
        return 'core'
    else:
        return 'install'


def get_blueprints(app):

    installConfig = get_config(app.config['INSTALL_FOLDER'])
    if installConfig.getboolean('Install', 'install'):
        from onyx.core.controllers.base import core
        from onyx.core.actions import action
        from onyx.core.controllers.auth import auth
        from onyx.core.controllers.api import api
        from onyx.core.widgets import widgets
        BLUEPRINTS = [core,auth,api,action,widgets]
        for module in plugin:
            try:
                BLUEPRINTS.append(module.get_blueprint())
            except:
                print('No Blueprint for module : ' + module.get_name())
        return BLUEPRINTS
    else:
        from onyx.core.controllers.install import install
        return install


def set_log():
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.INFO)
    logger.addHandler(steam_handler)


def create_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


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
    celery.config_from_object(app.config)

def gvars(app):
    server.app = app
    @app.before_request
    def get_vars():
        try:
            server.user = current_user.username
            server.lang = current_user.lang
            server.email = current_user.email
            server.id = current_user.id
            server.admin = current_user.admin
            server.get_vars()
        except:
            server.user = None
            server.lang = None
            server.email = None
            server.id = None
            server.admin = None
            server.get_vars()
    server.get_context(babel)

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
