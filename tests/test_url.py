# -*- coding: utf-8 -*-
from .common import ActivitiTestCase

class UrlTestCase(ActivitiTestCase):
    def test_user_url(self):
        user_id = 'user1'
        self.assertEqual(
            self.to_endpoint('identity', 'users', user_id),
            self.activiti.user_url(user_id)
        )

    def test_users_url(self):
        self.assertEqual(
            self.to_endpoint('identity', 'users'),
            self.activiti.users_url()
        )

    def test_group_url(self):
        group_id = 'group1'
        self.assertEqual(
            self.to_endpoint('identity', 'groups', group_id),
            self.activiti.group_url(group_id)
        )

    def test_groups_url(self):
        self.assertEqual(
            self.to_endpoint('identity', 'groups'),
            self.activiti.groups_url()
        )

    def test_deployments_url(self):
        self.assertEqual(
            self.to_endpoint('repository', 'deployments'),
            self.activiti.deployments_url()
        )

    def test_deployment_url(self):
        self.assertEqual(
            self.to_endpoint('repository', 'deployments', 10),
            self.activiti.deployment_url(10)
        )

