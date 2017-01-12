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



from flask import Flask, request, render_template , g , abort , redirect , url_for
from onyx.extensions import (db, mail, login_manager, babel, cache, celery)
from os import path
from flask_login import current_user
from os.path import dirname, abspath, join
from onyx.config import get_config
from onyx.api.server import *
from celery import Celery


#Log
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



__all__ = ('create_app', 'create_celery')

def create_app(config=None, app_name='onyx', blueprints=None):

    app = Flask(app_name,
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
        template_folder = 'templates'
    )
    app.config.from_object('onyx.flask_config')
    app.config.from_pyfile('../local.cfg', silent=True)
    if config:
        app.config.from_pyfile(config)

    extensions_fabrics(app)
    log()

    installConfig = get_config(app.config['INSTALL_FOLDER'])
    if installConfig.getboolean('Install', 'install'):
        from onyx.core.controllers.base import core
        from onyx.core.controllers.auth import auth
        from onyx.core.controllers.api import api
        from onyx.plugins import plugin
        BLUEPRINTS = [core,auth,api]
        for module in plugin:
            try:
                BLUEPRINTS.append(module.get_blueprint())
            except:
                print('No Blueprint for module : ' + module.get_name())

        blueprint_name = 'core'
    else:
        from onyx.core.controllers.install import install
        BLUEPRINTS = install
        blueprint_name = 'install'

    if blueprints is None:
        blueprints = BLUEPRINTS

    blueprints_fabrics(app, blueprints)



    error_pages(app , blueprint_name)
    gvars(app)


    with app.app_context():
        from migrate.versioning import api
        db.create_all()
        try:
            if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
                api.create(app.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
                api.version_control(app.config['SQLALCHEMY_DATABASE_URI'],app.config['SQLALCHEMY_MIGRATE_REPO'])
            else:
                api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'],
                                    api.version(app.config['SQLALCHEMY_MIGRATE_REPO']))
        except:
            pass
        logger.info("Initialized Database")


    logger.info('Onyx is ready !')
    return app

def log():
    LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
    from colorlog import ColoredFormatter
    formatter = ColoredFormatter(LOGFORMAT)
    """
    file_handler = RotatingFileHandler(os.path.join(os.path.dirname(__file__), '..', 'log/activity.log'), 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    """


    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)
    steam_handler.setFormatter(formatter)


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
    server = Server()
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
