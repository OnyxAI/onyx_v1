# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
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
from onyx.flask_config import TestConfig

from onyx.core.models.UsersModel import User
from flask.ext.login import login_user

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
    error_pages(app, get_blueprint_name(app))
    return TestApp(app)

@pytest.yield_fixture(scope='function')
def connected(app):
    """A Webtest app with connected user."""
    test = TestApp(app)

    user = User(username='Tony', email='tony@starkindustries.com')
    _db.session.add(user)
    _db.session.commit()

    login_user(user)
    user.authenticated = True

    yield test

    print('Done')


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()

@pytest.yield_fixture(scope='function')
def user_test_a(db):
    """A database for the tests."""
    user = User(username='Tony', email='tony@starkindustries.com', password='tony1234', admin=1)
    db.session.add(user)
    db.session.commit()

    yield user

    # Explicitly close DB connection
    db.session.close()
    db.drop_all()

@pytest.yield_fixture(scope='function')
def user_test(db):
    """A database for the tests."""
    user = User(username='Pepper', email='pepper@starkindustries.com', password='pepper1234')
    db.session.add(user)
    db.session.commit()

    yield user

    # Explicitly close DB connection
    db.session.close()
    db.drop_all()
