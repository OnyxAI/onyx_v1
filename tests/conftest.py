# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest

from webtest import TestApp
from onyx import *
from onyx.extensions import db as _db
from onyx.app_config import TestConfig

from onyx.core.models.UsersModel import User
from onyx.core.models.ConfigModel import Config

from flask import session
from flask_login import login_user
from flask_jwt_extended import create_access_token, create_refresh_token

from passlib.hash import sha256_crypt

@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(config=TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    blueprints_fabrics(app, get_blueprints(app))
    error_pages(app)

    return TestApp(app)

@pytest.yield_fixture(scope='function')
def connected_admin_app(app):
    """A Webtest app with connected admin user."""
    test_app = TestApp(app)

    user = User(username='Admin', email='admin@starkindustries.com', password=sha256_crypt.hash("123456"), admin=1)
    _db.session.add(user)
    _db.session.commit()

    access_token = create_access_token(identity = user.as_dict())
    refresh_token = create_refresh_token(identity = user.as_dict())

    test_app.authorization = ('Bearer', access_token)

    login_user(user)
    user.authenticated = True

    yield test_app

@pytest.yield_fixture(scope='function')
def connected_app(app):
    """A Webtest app with connected user."""
    test_app = TestApp(app)

    user = User(username='User', email='user@starkindustries.com', password=sha256_crypt.hash("123456"), admin=0)
    _db.session.add(user)
    _db.session.commit()

    access_token = create_access_token(identity = user.as_dict())
    refresh_token = create_refresh_token(identity = user.as_dict())

    test_app.authorization = ('Bearer', access_token)

    login_user(user)
    user.authenticated = True

    yield test_app


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    query = Config(config='install', value='True')
    _db.session.add(query)
    _db.session.commit()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()

@pytest.yield_fixture(scope='function')
def user_test_a(db):
    """A database for the tests."""
    user = User(username='Tony', email='tony@starkindustries.com', password=sha256_crypt.hash("tony1234"), admin=1)
    db.session.add(user)
    db.session.commit()

    yield user

    # Explicitly close DB connection
    db.session.close()
    db.drop_all()

@pytest.yield_fixture(scope='function')
def user_test(db):
    """A database for the tests."""
    user = User(username='Pepper', email='pepper@starkindustries.com', password=sha256_crypt.hash("pepper1234"))
    db.session.add(user)
    db.session.commit()

    yield user

    # Explicitly close DB connection
    db.session.close()
    db.drop_all()
