# -*- coding: utf-8 -*-
import json
from requests.status_codes import codes
import requests_mock

from .common import ActivitiTestCase
from pyactiviti import exceptions

class UserTestCase(ActivitiTestCase):
    @requests_mock.mock()
    def test_user_does_not_exist(self, mock):
        mock.get(
            self.activiti.user_url(('user1')),
            status_code=codes.not_found
        )

        self.assertFalse(self.activiti.user_exists('user1'))

    @requests_mock.mock()
    def test_user_exists(self, mock):
        mock.get(
            self.activiti.user_url('user1'),
            status_code=codes.ok
        )

        self.assertTrue(self.activiti.user_exists('user1'))

    @requests_mock.mock()
    def test_get_user(self, mock):
        user_id = 'user1'
        fake_user = self.fake_user(user_id)
        mock.get(
            self.activiti.user_url(user_id),
            content=json.dumps(fake_user),
            status_code=codes.ok
        )
        remote_user = self.activiti.get_user(user_id)
        self.assertEqual(fake_user, remote_user)

    def fake_user(self, login):
        return {
            'id': login,
            'firstName': 'firstName',
            'lastName': 'lastName',
            'url': self.activiti.user_url(login)
        }

    @requests_mock.mock()
    def test_users(self, mock):
        fake_users = {
            'total': 2,
            'size': 2,
            'sort': 'id',
            'order': 'asc',
            'data': [
                self.fake_user(u'user1'),
                self.fake_user(u'user2'),
            ]
        }

        mock.get(
            self.activiti.users_url(),
            headers={'Content-Type': 'application/json'},
            status_code=codes.ok,
            content=json.dumps(fake_users)
        )

        result = self.activiti.users()['data']
        self.assertEqual(len(result), len(fake_users['data']))
        self.assertEqual(result, fake_users['data'])

    @requests_mock.mock()
    def test_create_user(self, mock):
        fake_user = self.fake_user('user1')
        mock.post(
            self.activiti.users_url(),
            content=json.dumps(fake_user),
            status_code=codes.created,
        )

        user = self.activiti.create_user('user1', 'foo@bar.org', 'secret')

        self.assertEqual(user, fake_user)

    @requests_mock.mock()
    def test_create_user_conflict(self, mock):
        mock.post(
            self.activiti.users_url(),
            status_code=codes.conflict,
            content=json.dumps({'exception': 'Exception'})
        )

        with self.assertRaises(exceptions.UserAlreadyExists):
            self.activiti.create_user('user1', 'foo@bar.org', 'secret')

    @requests_mock.mock()
    def test_create_user_missing_id(self, mock):
        mock.post(
            self.activiti.users_url(),
            status_code=codes.bad_request,
        )
        with self.assertRaises(exceptions.UserMissingID):
            self.activiti.create_user(None, 'foo@bar.org', 'secret')

    @requests_mock.mock()
    def test_delete_user(self, mock):
        mock.delete(
            self.activiti.user_url('user1'),
            status_code=codes.no_content,
        )
        self.assertTrue(self.activiti.delete_user('user1'))

    @requests_mock.mock()
    def test_delete_user_not_found(self, mock):
        mock.delete(
            self.activiti.user_url('user1'),
            status_code=codes.not_found
        )
        with self.assertRaises(exceptions.UserNotFound):
            self.activiti.delete_user('user1')

    @requests_mock.mock()
    def test_update_user(self, mock):
        update = {
            'firstName': 'Tijs',
            'lastName': 'Barrez',
            'email': 'no-reply@alfresco.org',
            'password': 'pass123',
        }

        mock.put(
            self.activiti.user_url('user1'),
            status_code=codes.ok,
            content=json.dumps(update),
        )

        response = self.activiti.user_update('user1', update)
        self.assertDictEqual(response, update)

    @requests_mock.mock()
    def test_update_user_not_found(self, mock):
        mock.put(
            self.activiti.user_url('user1'),
            status_code=codes.not_found,
        )
        with self.assertRaises(exceptions.UserNotFound):
            self.activiti.user_update('user1', {})

    @requests_mock.mock()
    def test_update_user_updated_simultaneous(self, mock):
        mock.put(
            self.activiti.user_url('user1'),
            status_code=codes.conflict
        )
        with self.assertRaises(exceptions.UserUpdatedSimultaneous):
            self.activiti.user_update('user1', {})
