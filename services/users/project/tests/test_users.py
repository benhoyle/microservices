"""Tests for user details."""
# services/users/project/tests/test_users.py

import json
import unittest

from project import db
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from project.api.models import User


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

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

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'ben',
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json',
                headers=self.get_token_header()
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('ben@ben.org was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
                headers=self.get_token_header()
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error if the JSON object does not have a username key."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'ben@ben.org'}),
                content_type='application/json',
                headers=self.get_token_header()
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        headers = self.get_token_header()
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'ben',
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json',
                headers=headers
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'ben',
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json',
                headers=headers
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('ben', 'ben@ben.org', '123456')
        with self.client:
            response = self.client.get('/users/{}'.format(user.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('ben', data['data']['username'])
            self.assertIn('ben@ben.org', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if no id is provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if id does not exist"""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('ben', 'ben@ben.org', '123456')
        add_user('jimbob', 'jim@bob.org.uk', '123456')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('ben', data['data']['users'][0]['username'])
            self.assertIn('jimbob', data['data']['users'][1]['username'])
            self.assertIn('ben@ben.org', data['data']['users'][0]['email'])
            self.assertIn('jim@bob.org.uk', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        add_user('ben', 'ben@ben.org', '123456')
        add_user('jimbob', 'jim@bob.org.uk', '123456')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'ben', response.data)
            self.assertIn(b'jimbob', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='ben', email='ben@ben.org', password='123'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'ben', response.data)

    def test_add_user_invalid_json_keys_no_password(self):
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

    def test_add_user_inactive(self):
        """Test an inactive user adding a user."""
        headers = self.get_token_header()
        user = User.query.filter_by(email='admin@admin.org').first()
        user.active = False
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'ben',
                    'email': 'ben@ben.org',
                    'password': '123456'
                }),
                content_type='application/json',
                headers=headers
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
