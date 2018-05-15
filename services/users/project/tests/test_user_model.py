"""Tests for users database objects."""
# services/users/project/tests/test_user_model.py

import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    """Test user model."""

    def test_add_user(self):
        """Test adding a user."""
        user = add_user('justatest', 'test@test.com', '123456')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        """Test adding a user with a duplicate username."""
        add_user('justatest', 'test@test.com', '123456')
        duplicate_user = User(
            username='justatest',
            email='test@test2.com',
            password='123456'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        """Test adding a user with a duplicate email."""
        add_user('justatest', 'test@test.com', '123456')
        duplicate_user = User(
            username='justanothertest',
            email='test@test.com',
            password='123456'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        """Test converting an object to JSON."""
        user = add_user('justatest', 'test@test.com', '123456')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        """Test passwords are random."""
        user_one = add_user('justatest', 'test@test.com', 'greaterthaneight')
        user_two = add_user('justatest2', 'test@test2.com', 'greaterthaneight')
        self.assertNotEqual(user_one.password, user_two.password)

if __name__ == "__main__":
    unittest.main()
