# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest
from flask import url_for

from onyx.extensions import db
from onyx.core.models.UsersModel import User
from flask.ext.login import login_user

@pytest.mark.usefixtures('db','testapp','connected')
class TestAuthController:
    """Controller tests."""

    def test_hello_returns_200(self, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get(url_for('auth.hello'))
        assert res.status_code == 200

    def test_login_returns_200(self, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get(url_for('auth.login'))
        assert res.status_code == 200

    def test_register_returns_200(self, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get(url_for('auth.register'))
        assert res.status_code == 200
