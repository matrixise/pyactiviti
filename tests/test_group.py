# -*- coding: utf-8 -*-
import json
from requests.status_codes import codes
import requests_mock

from .common import ActivitiTestCase
from pyactiviti import exceptions

class GroupTestCase(ActivitiTestCase):
    @requests_mock.mock()
    def test_001_create_group(self, mock):
        fake_group = {
            'id': 'group1',
            'name': 'Group1',
            'type': 'Type',
        }
        mock.post(
            self.activiti.groups_url(),
            content=json.dumps(fake_group),
            status_code=codes.created,
        )
        group = self.activiti.create_group('group1', 'Group1', 'Type')
        self.assertDictEqual(fake_group, group)

    @requests_mock.mock()
    def test_002_create_group_missing_id(self, mock):
        fake_group = {}
        mock.post(
            self.activiti.groups_url(),
            content=json.dumps(fake_group),
            status_code=codes.bad_request,
        )
        with self.assertRaises(exceptions.GroupMissingID):
            self.activiti.create_group(None, 'Group1', 'Type')

    @requests_mock.mock()
    def test_003_get_group(self, mock):
        mock.get(
            self.activiti.group_url('group1'),
            status_code=codes.ok
        )
        self.assertTrue(self.activiti.get_group('group1'))

    @requests_mock.mock()
    def test_004_get_group_does_not_exist(self, mock):
        mock.get(
            self.activiti.group_url('group1'),
            status_code=codes.not_found
        )
        self.assertFalse(self.activiti.get_group('group1'))

    @requests_mock.mock()
    def test_005_delete_group(self, mock):
        mock.delete(
            self.activiti.group_url('group1'),
            status_code=codes.no_content,
        )
        self.assertTrue(self.activiti.delete_group('group1'))

    @requests_mock.mock()
    def test_006_delete_group_exception(self, mock):
        mock.delete(
            self.activiti.group_url('group1'),
            status_code=codes.not_found,
        )
        with self.assertRaises(exceptions.GroupNotFound):
            self.activiti.delete_group('group1')

    @requests_mock.mock()
    def test_007_groups(self, mock):
        fake_groups = {
            'data': [
                {
                    'id': 'testgroup',
                    'url': self.activiti.group_url('testgroup'),
                    'name': 'Test Group',
                    'type': 'Test Type',
                }
            ],
            'total': 1,
            'size': 1,
            'sort': 'id',
            'order': 'asc',
        }
        mock.get(
            self.activiti.groups_url(),
            status_code=codes.ok,
            content=json.dumps(fake_groups),
        )

        result = self.activiti.groups()
        self.assertEqual(result['size'], 1)
        self.assertEqual(result['data'], fake_groups['data'])

    @requests_mock.mock()
    def test_008_update_group(self, mock):
        update = {
            'name': 'Test group',
            'type': 'Test type',
        }
        mock.put(
            self.activiti.group_url('group1'),
            status_code=codes.ok,
            content=json.dumps(update)
        )
        self.assertEqual(self.activiti.group_update('group1', update), update)

    @requests_mock.mock()
    def test_009_update_group_not_found(self, mock):
        mock.put(
            self.activiti.group_url('group1'),
            status_code=codes.not_found
        )
        with self.assertRaises(exceptions.GroupNotFound):
            self.activiti.group_update('group1', {})

    @requests_mock.mock()
    def test_010_update_group_updated_simultaneous(self, mock):
        mock.put(
            self.activiti.group_url('group1'),
            status_code=codes.conflict,
        )
        with self.assertRaises(exceptions.GroupUpdatedSimultaneous):
            self.activiti.group_update('group1', {})

    def endpoint_group_members(self, group_id):
        return self.to_endpoint('identity', 'groups', group_id, 'members')

    @requests_mock.mock()
    def test_011_add_member_to_group(self, mock):
        group_id, user_id = 'group1', 'user1'

        fake_response = {
            'userId': user_id,
            'groupId': group_id,
            'url': self.endpoint_group_members_user(group_id, user_id),
        }

        mock.post(
            self.endpoint_group_members(group_id),
            status_code=codes.created,
            content=json.dumps(fake_response)
        )

        response = self.activiti.group_add_member(group_id, user_id)
        self.assertDictEqual(response, fake_response)

    @requests_mock.mock()
    def test_011_add_member_to_group_not_found(self, mock):
        group_id, user_id = 'group1', 'user1'

        mock.post(
            self.endpoint_group_members(group_id),
            status_code=codes.not_found,
        )

        with self.assertRaises(exceptions.GroupNotFound):
            self.activiti.group_add_member(group_id, user_id)

    @requests_mock.mock()
    def test_011_add_member_to_group_already_member(self, mock):
        group_id, user_id = 'group1', 'user1'

        mock.post(
            self.endpoint_group_members(group_id),
            status_code=codes.conflict,
        )

        with self.assertRaises(exceptions.UserAlreadyMember):
            self.activiti.group_add_member(group_id, user_id)

    def endpoint_group_members_user(self, group_id, user_id):
        return self.to_endpoint('identity', 'groups', group_id, 'members', user_id)

    @requests_mock.mock()
    def test_012_remove_member_from_group(self, mock):
        group_id, user_id = 'group1', 'user1'
        mock.delete(
            self.endpoint_group_members_user(group_id, user_id),
            status_code=codes.no_content

        )
        self.assertTrue(self.activiti.group_remove_member(group_id, user_id))

    @requests_mock.mock()
    def test_012_remove_member_from_group_not_found(self, mock):
        group_id, user_id = 'group1', 'user1'
        mock.delete(
            self.endpoint_group_members_user(group_id, user_id),
            status_code=codes.not_found

        )
        with self.assertRaises(exceptions.NotFound):
            self.activiti.group_remove_member(group_id, user_id)