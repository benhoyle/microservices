"""Tests for authentication."""
# services/users/project/tests/test_auth.py

import json
from flask import current_app

from project import db
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from project.api.models import User


class TestAuthBlueprint(BaseTestCase):
    """Test authentication blueprint."""

    def get_token_header(self):
        """Add user and login to get a token."""
        add_user('admin', 'admin@admin.org', '123456')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'admin@admin.org',
                'password': '123456'
            }),
            content_type='application/json'
        )
        token = json.loads(resp_login.data.decode())['auth_token']
        return {'Authorization': 'Bearer {token}'.format(token=token)}

    def test_user_registration(self):
        """Test user registration."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'ben',
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        add_user('ben', 'ben@ben.org', '123456')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'ben2',
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_duplicate_username(self):
        """Ensure error is thrown if the username already exists."""
        add_user('ben', 'ben@ben.org', '123456')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'ben',
                    'email': 'ben@ben2.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        """
        Ensure error is thrown if the JSON object does
        not have a username key.
        """
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email='ben@test.org',
                    password='123'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        """
        Ensure error is thrown if the JSON object does
        not have a username key.
        """
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='ben',
                    password='123'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object does
        not have a password key.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='ben',
                    email='ben@test.org'
                )),
                content_type='application/json',
                headers=self.get_token_header()
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_registered_user_login(self):
        """Test login of a registered user."""
        add_user('ben', 'ben@ben.org', '123456')
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        """Test login of an unregistered user."""
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        """Test valid logout."""
        add_user('ben', 'ben@ben.org', '123456')
        with self.client:
            # Login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer {token}'.format(token=token)}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        """Test invalid logout with expired token."""
        add_user('ben', 'ben@ben.org', '123456')
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        with self.client:
            # Login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            # invalid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer {token}'.format(token=token)}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        """Test invalid logout."""
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        """Test obtaining status of a user."""
        add_user('ben', 'ben@ben.org', '123456')
        with self.client:
            # Login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer {token}'.format(token=token)}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'ben')
            self.assertTrue(data['data']['email'] == 'ben@ben.org')
            self.assertTrue(data['data']['active'])
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        """Test an invalid request for a status of a user."""
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        """Test a logout with an inactive user."""
        add_user('ben', 'ben@ben.org', '123456')
        # Update user
        user = User.query.filter_by(email='ben@ben.org').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer {token}'.format(token=token)}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_status_inactive(self):
        """Test accessing status if user is inactive."""
        add_user('ben', 'ben@ben.org', '123456')
        # Update user
        user = User.query.filter_by(email='ben@ben.org').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer {token}'.format(token=token)}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)
