"""Utilities for testing."""
# services/users/project/tests/utils.py

from project import db
from project.api.models import User


def add_user(username, email, password):
    """Add a user."""
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user
