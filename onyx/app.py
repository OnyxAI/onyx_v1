# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import importlib
from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_jwt_extended import JWTManager
from onyx.extensions import (db, login_manager, babel, cache)
from flask_login import current_user
from onyx.config import get_config
from onyx.api.assets import Json
from onyx.api.server import *
from onyx.util.log import getLogger
from onyx.skills.core import *
import threading

#from onyx.api.kernel import Kernel

from onyx.sockyx.client.ws import WebsocketClient
from onyx.sockyx.message import Message

from onyx.core.models import ConfigModel, RevokedTokenModel

server = Server()
LOG = getLogger("App")
json = Json()
#kernel = Kernel()

to_reload = False

from onyx.app_config import ProdConfig, Config


__all__ = ('create_app', 'create_db', 'blueprints_fabrics', 'get_blueprints', 'error_pages', 'ws', 'AppReloader')

class AppReloader(object):
    def __init__(self, create):
        self.create = create
        self.app = create()

    def get_application(self):
        global to_reload
        if to_reload:
            self.app = self.create()
            to_reload = False

        return self.app

    def __call__(self, environ, start_response):
        app = self.get_application()
        return app(environ, start_response)


def create_app(config=ProdConfig, app_name='onyx', blueprints=None):

    app = Flask(app_name,
        static_folder = 'static',
        template_folder = 'templates'
    )

    app.config.from_pyfile('../local.cfg', silent=True)
    if config:
        app.config.from_object(config)

    extensions_fabrics(app)

    jwt = JWTManager(app)

    gvars(app, jwt)

    blueprints_fabrics(app, get_blueprints(app))
    error_pages(app)

    with app.app_context():
        db.create_all()

    @app.route('/reload/<next>')
    def reload(next):
        global to_reload
        to_reload = True

        return redirect(url_for(next))
        
    return app

def create_db(config=ProdConfig, app_name='onyx', blueprints=None):

    app = Flask(app_name,
        static_folder = 'static',
        template_folder = 'templates'
    )
    

    app.config.from_pyfile('../local.cfg', silent=True)
    if config:
        app.config.from_object(config)

    extensions_fabrics(app)

    with app.app_context():
        db.create_all()

    
        
    return app

def create_ws(app):
    with app.app_context():
        ws_app = ws()
        ws_app.run_forever()

def ws():
    ws = WebsocketClient()
    return ws


def get_blueprints(app):

    from onyx.core.controllers.base import core
    from onyx.core.actions import action
    from onyx.core.controllers.auth import auth
    from onyx.core.controllers.api import api
    from onyx.core.widgets import widgets
    from onyx.core.controllers.install import install
    

    BLUEPRINTS = [core, auth, api, action, widgets]

    all_skills = get_blueprint(app.config['SKILL_FOLDER'])
    for skill in all_skills:
        if (hasattr(skill, 'create_skill') and callable(skill.create_skill)):
            Module = skill.create_skill()
            if (hasattr(Module, 'get_blueprint') and callable(Module.get_blueprint)):
                BLUEPRINTS.append(Module.get_blueprint())


    for blueprint in BLUEPRINTS:
        @blueprint.before_request
        def check_base_db():
            install = ConfigModel.Config.query.filter_by(config='install').first()
            if install == None:
                query = ConfigModel.Config(config='install', value='False')
                db.session.add(query)
                db.session.commit()
                return redirect(url_for('install.index'))
            elif install.value == 'False':
                return redirect(url_for('install.index'))
                
    BLUEPRINTS.append(install)
    return BLUEPRINTS


def blueprints_fabrics(app, blueprints):
    """Configure blueprints in views."""
    try:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
    except:
        app.register_blueprint(blueprints)

    

def extensions_fabrics(app):
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    #cache.init_app(app)

def error_pages(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("404.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("500.html"), 500

def gvars(app, jwt):

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.RevokedToken.is_jti_blacklisted(jti)

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
           
            return json.decode(execute.get_data().decode('utf8'))
        return dict(get_params=get_params)

    @app.context_processor
    def utility_processor():
        def get_variable(p,variable):
            v = str(variable.encode('ascii'))
            return p[v]
        return dict(get_variable=get_variable)

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
            raw_lang = g.lang
            if raw_lang:
                lang = raw_lang.split('-')
                if lang[0] in Config.ACCEPT_LANGUAGES:
                    return lang[0]
                else:
                    return Config.BABEL_DEFAULT_LOCALE
            else:
                return 'en'
    except AssertionError:
        pass
