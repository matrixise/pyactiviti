# -*- coding: utf-8 -*-
import json
import contextlib
import StringIO

from requests.status_codes import codes
import requests_mock

from .common import ActivitiTestCase
from pyactiviti import exceptions

class DeploymentTestCase(ActivitiTestCase):
    @requests_mock.mock()
    def test_deployments(self, mock):
        fake_deployments = {
            'data': [
                {
                    "id": "10",
                    "name": "activiti-examples.bar",
                    "deploymentTime": "2010-10-13T14:54:26.750+02:00",
                    "category": "examples",
                    "url": self.activiti.deployment_url(10),
                    "tenantId": None
                }
            ],
            "total": 1,
            "start": 0,
            "sort": "id",
            "order": "asc",
            "size": 1
        }

        mock.get(
            self.activiti.deployments_url(),
            status_code=codes.ok,
            content=json.dumps(fake_deployments)
        )

        response = self.activiti.deployments()

        self.assertEqual(response['total'], 1)

    @requests_mock.mock()
    def test_get_deployment(self, mock):
        fake_deployment = {
            "id": "10",
            "name": "activiti-examples.bar",
            "deploymentTime": "2010-10-13T14:54:26.750+02:00",
            "category": "examples",
            "url": self.activiti.deployment_url(10),
            "tenantId" : None
}
        mock.get(
            self.activiti.deployment_url(10),
            content=json.dumps(fake_deployment),
            status_code=codes.ok
        )

        deployment = self.activiti.get_deployment(10)
        self.assertDictEqual(fake_deployment, deployment)

    @requests_mock.mock()
    def test_get_deployment_not_found(self, mock):
        mock.get(
            self.activiti.deployment_url(10),
            status_code=codes.not_found
        )

        with self.assertRaises(exceptions.DeploymentNotFound):
            self.activiti.get_deployment(10)

    # @requests_mock.mock()
    # def test_create_deployment(self, mock):
    #     mock.post(
    #         self.activiti.deployments_url(),
    #         status_code=codes.ok,
    #     )
    #
    #     with contextlib.closing(StringIO.StringIO()) as strIO:
    #         self.assertTrue(self.activiti.create_deployment(strIO))
    #
    # @requests_mock.mock()
    # def test_create_deployment(self, mock):
    #     mock.post(
    #         self.activiti.deployments_url(),
    #         status_code=codes.bad_request,
    #     )
    #
    #     with contextlib.closing(StringIO.StringIO()) as strIO:
    #         self.assertTrue(self.activiti.create_deployment(None))