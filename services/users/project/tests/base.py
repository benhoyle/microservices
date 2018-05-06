"""Base testing file."""
# services/users/project/tests/base.py

from flask_testing import TestCase

from project import app, db


class BaseTestCase(TestCase):
    """Base Test Case."""
    
    def create_app(self):
        """App creation for tests."""
        app.config.from_object('project.config.TestingConfig')
        return app

    def setUp(self):
        """Setup tests."""
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """Operations for testing shutdown."""
        db.session.remove()
        db.drop_all()
