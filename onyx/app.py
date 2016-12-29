"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
# -*- coding: utf-8 -*-
import os
import sys
try:
    import Onyx
    sys.path.append(str(Onyx.__path__[0]))
except:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, render_template , g , abort , redirect , url_for
from onyx.extensions import (db, mail, pages, manager, login_manager, babel, csrf, cache, celery)
from os import path
from flask_login import current_user
from os.path import dirname, abspath, join
from onyx.config import get_config
from onyx.api.server import *

#from onyx.plugins.speak import speak
#speak('Bonjour bienvenue sur Onyx')

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

    installConfig = get_config('install')
    if installConfig.getboolean('Install', 'install'):
        from onyx.core.controllers.base import core
        from onyx.core.controllers.auth import auth
        from onyx.plugins import plugin
        BLUEPRINTS = [core,auth]
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
            print("Migrate Already Done")
        print ("Base de donnee initialisee")
        

    from onyx.plugins import plugin
    for module in plugin:
        try:
            module.init(app)
        except:
            module.init()


    return app
  
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
    pages.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)


def gvars(app):

    getG(app)
    getContext(app,babel)

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


