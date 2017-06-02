# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

"""Application configuration."""
import os
import onyx
import configparser

class Config(object):
    """Base configuration."""
    ONYX_PATH = onyx.__path__[0]
    SKILL_FOLDER = ONYX_PATH + "/skills/"
    DATA_FOLDER = ONYX_PATH + "/data/"
    CONFIG = configparser.ConfigParser()
	CONFIG.read(ONYX_PATH + "/config/onyx.cfg")
    INSTALL = CONFIG.getboolean('Install', 'done')
    LANG = CONFIG.get('Base', 'lang')
    SECRET_KEY = 'change me please'
    SECURITY_PASSWORD_SALT= 'change me please'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # default babel values
    BABEL_DEFAULT_LOCALE = 'fr'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    ACCEPT_LANGUAGES = ['en', 'fr' ]
    # available languages
    LANGUAGES = {
        'en': u'English',
        'fr': u'Français'
    }


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + Config.ONYX_PATH + "/db/data.db"
    SQLALCHEMY_MIGRATE_REPO = Config.ONYX_PATH + "/db/db_repository"
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    # Put the db file in project root
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + Config.ONYX_PATH + "/db/data.db"
    SQLALCHEMY_MIGRATE_REPO = Config.ONYX_PATH + "/db/db_repository"
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
