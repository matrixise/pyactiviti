# -*- coding: utf-8 -*-
import requests
import json
from requests.status_codes import codes

from .exceptions import (
    UserAlreadyExists,
    NotFound,
    UserNotFound,
    GroupNotFound,
    GroupMissingID,
    UserMissingID,
    GroupUpdatedSimultaneous,
    UserAlreadyMember,
    UserUpdatedSimultaneous,
    DeploymentNotFound
)

USERS_FIELDS = [
    'id', 'firstName', 'lastNAme', 'email', 'firstNameLike',
    'lastNameLike', 'emailLike', 'memberOfGroup', 'potentialStarter',
    'sort'
]


GROUPS_FIELDS = [
    'id', 'name', 'type', 'nameLike', 'member', 'potentialStarter', 'sort'
]

DEPLOYMENTS_FIELDS = [
    'name', 'nameLike', 'category', 'categoryNotEquals', 'tenantId',
    'tenantIdLike', 'withoutTenantId', 'sort'
]


def check_parameters(fields, args):
    arguments = {}
    for item in fields:
        value = args.pop(item, None)
        if value:
            arguments[item] = value
    return arguments


class Activiti(object):
    def __init__(self, endpoint, auth=('kermit', 'kermit')):
        self.endpoint = endpoint
        self.auth = auth

        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({'content-type': 'application/json'})

    user_url = lambda self, id: self.users_url(id)
    group_url = lambda self, id: self.groups_url(id)

    def user_exists(self, login):
        response = self._get(self.user_url(login))
        return response.status_code == codes.ok

    def get_user(self, login):
        response = self._get(self.user_url(login))
        if response.status_code == codes.ok:
            return response.json()
        raise UserNotFound()

    def users_url(self, *args):
        return self._to_endpoint('identity', 'users', *args)

    def users(self, **parameters):
        params = check_parameters(USERS_FIELDS, parameters)

        response = self._get(self.users_url(), params=params)
        if response.status_code == codes.ok:
            return response.json()
        raise NotImplementedError()

    def get_users_member_of(self, group):
        return self.users(memberOfGroups=group)

    def create_user(self, login, email, password, firstname=None, lastname=None):
        user = {
            'id': login,
            'email': email,
            'password': password,
            'firstName': firstname or '',
            'lastName': lastname or ''
        }
        response = self._post(self.users_url(), user)
        if response.status_code == codes.created:
            return response.json()
        elif response.status_code == codes.conflict:
            raise UserAlreadyExists(response.json()['exception'])
        elif response.status_code == codes.bad_request:
            raise UserMissingID()

        return response.status_code == codes.created

    def user_update(self, user_id, values=None):
        response = self._put(self.user_url(user_id), values=values)
        if response.status_code == codes.ok:
            return response.json()
        elif response.status_code == codes.not_found:
            raise UserNotFound()
        elif response.status_code == codes.conflict:
            raise UserUpdatedSimultaneous()

    def delete_user(self, login):
        response = self._delete(self.user_url(login))
        if response.status_code == codes.no_content:
            return True
        elif response.status_code == codes.not_found:
            raise UserNotFound()

    def groups_url(self, *args):
        return self._to_endpoint('identity', 'groups', *args)

    def get_group(self, group_id):
        response = self._get(self.group_url(group_id))
        if response.status_code == codes.ok:
            return True
        elif response.status_code == codes.not_found:
            return False
        raise NotImplementedError()

    def groups(self, **parameters):
        params = check_parameters(GROUPS_FIELDS, parameters)

        response = self._get(self.groups_url(), params=params)
        if response.status_code == codes.ok:
            return response.json()

        raise NotImplementedError()

    def group_update(self, group_id, values=None):
        response = self._put(self.group_url(group_id), values=values)
        if response.status_code == codes.ok:
            return response.json()
        elif response.status_code == codes.not_found:
            raise GroupNotFound()
        elif response.status_code == codes.conflict:
            raise GroupUpdatedSimultaneous()

    def create_group(self, id, name, type):
        values = dict(id=id, name=name, type=type)
        response = self._post(self.groups_url(), values)
        if response.status_code == codes.created:
            return response.json()
        elif response.status_code == codes.bad_request:
            raise GroupMissingID()

    def delete_group(self, group_id):
        response = self._delete(self.group_url(group_id))

        if response.status_code == codes.no_content:
            return True
        elif response.status_code == codes.not_found:
            raise GroupNotFound()

    def group_add_member(self, group_id, user_id):
        values = {
            'userId': user_id,
        }
        response = self._post(
            self._to_endpoint('identity', 'groups', group_id, 'members'),
            values=values
        )
        if response.status_code == codes.created:
            return response.json()
        elif response.status_code == codes.not_found:
            raise GroupNotFound()
        elif response.status_code == codes.conflict:
            raise UserAlreadyMember()

    def group_remove_member(self, group_id, user_id):
        response = self._delete(
            self._to_endpoint('identity', 'groups', group_id, 'members', user_id)
        )
        if response.status_code == codes.no_content:
            return True
        elif response.status_code == codes.not_found:
            raise NotFound()

    def process_definitions(self):
        response = self._get('/repository/process-definitions')
        return json.loads(response.content)

    def _delete(self, service):
        return self.session.delete(service)

    def _post(self, service, values=None):
        if values:
            values = json.dumps(values)
        return self.session.post(service, data=values)

    def _get(self, service, params=None):
        return self.session.get(service, params=params)

    def _put(self, service, values=None):
        if values:
            values = json.dumps(values)
        return self.session.put(service, data=values)

    def _to_endpoint(self, *args):
        return '/'.join([self.endpoint, 'service'] + list(str(arg) for arg in args))

    def start_process_by_key(self, key, variables=None):
        if variables is None:
            variables = {}

        variables = [
            {'name': _key, 'value': value}
            for _key, value in variables.iteritems()
        ]
        values = {
            'processDefinitionKey': key,
            'businessKey': 'business%s' % key,
            'variables': variables,
        }
        return self._post('/runtime/process-instances', values)

    def get_user_task_list(self, user, process=None):
        url = '/runtime/tasks?involvedUser=%s' % (user,)
        if process:
            url += '&processDefinitionKey=%s' % (process,)

        response = self._get(url)
        return json.loads(response.content)

    def get_task_form(self, task_id):
        response = self._get('/form/form-data?taskId=%s' % (task_id,))
        return json.loads(response.content)

    def submit_task_form(self, task_id, properties=None):
        if properties is None:
            properties = {}

        properties = [
            {'id': _key, 'value': value}
            for _key, value in properties.iteritems()
        ]

        values = {
            'taskId': task_id,
            'properties': properties,
        }
        return self._post('/form/form-data', values)

    # Keep the backward-compatibility
    submitTaskForm = submit_task_form
    getTaskForm = get_task_form
    startProcessByKey = start_process_by_key
    getUserTaskList = get_user_task_list

    def deployments_url(self, *args):
        return self._to_endpoint('repository', 'deployments', *args)

    def deployment_url(self, deployment_id):
        return self.deployments_url(deployment_id)

    def deployments(self, **parameters):
        response = self._get(self.deployments_url(), params=parameters)
        if response.status_code == codes.ok:
            return response.json()
        raise NotImplementedError()

    def get_deployment(self, deployment_id):
        response = self._get(self.deployment_url(deployment_id))
        if response.status_code == codes.ok:
            return response.json()
        elif response.status_code == codes.not_found:
            raise DeploymentNotFound()
        raise NotImplementedError()

    # def create_deployment(self, files):
    #     response = self.session.post(self.deployments_url(), files=files)
