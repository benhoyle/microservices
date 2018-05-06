"""Tests for app configuration."""
# services/users/project/tests/test_config.py

import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    """Testing the development configuration."""

    def create_app(self):
        """App creation for tests."""
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """Test development settings."""
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )


class TestTestingConfig(TestCase):
    """Testing the testing configuration."""

    def create_app(self):
        """App creation for tests."""
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """Test testing settings."""
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )


class TestProductionConfig(TestCase):
    """Testing the development configuration."""

    def create_app(self):
        """App creation for tests."""
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """Test production settings."""
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
