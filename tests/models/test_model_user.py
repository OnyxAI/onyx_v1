# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest
from flask import url_for

from onyx.core.models.UsersModel import User
from factories import UserFactory


@pytest.mark.usefixtures('db','testapp')
class TestUser:
    """User tests."""

    def test_get_by_id(self, db):
        """Get user by ID."""
        user = User(username='foo', email='foo@bar.com')
        db.session.add(user)
        db.session.commit()

        retrieved = User.query.filter_by(id=user.id).first()
        assert retrieved == user

    def test_password_is_nullable(self, db):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        db.session.add(user)
        db.session.commit()

        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
