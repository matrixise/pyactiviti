import unittest
from pyactiviti import pyactiviti

ACTIVITI_AUTH = ('kermit', 'kermit')
ACTIVITI_SERVICE = 'http://localhost:8080/activiti-rest'

class ActivitiTestCase(unittest.TestCase):
    def setUp(self):
        self.activiti = pyactiviti.Activiti(ACTIVITI_SERVICE, auth=ACTIVITI_AUTH)
        self.to_endpoint = self.activiti._to_endpoint
