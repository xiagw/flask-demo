import json
from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    def test_users(self):
        """确保ping的服务正常."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """确保能够正确添加一个用户的用户到数据库中"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(
                    dict(username='cnych', email='abcd@gmail.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('abcd@gmail.com was added', data['message'])
            self.assertEqual('success', data['status'])

    def test_add_user_invalid_json(self):
        """如果JSON对象为空，确保抛出一个错误。"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertEqual('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """如果JSON对象中没有username或email，确保抛出一个错误。"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email='abcd@gmail.com')),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertEqual('fail', data['status'])

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(username='cnych')),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertEqual('fail', data['status'])

    def test_add_user_duplicate_user(self):
        """如果邮件已经存在确保抛出一个错误。"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='cnych',
                    email='abcd@gmail.com'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='cnych',
                    email='abcd@gmail.com'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertEqual('fail', data['status'])
