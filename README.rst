===============================
PyActiviti
===============================

.. image:: https://img.shields.io/travis/matrixise/pyactiviti.svg
        :target: https://travis-ci.org/matrixise/pyactiviti

.. image:: https://img.shields.io/pypi/v/pyactiviti.svg
        :target: https://pypi.python.org/pypi/pyactiviti


An SDK that helps with interacting with Activiti.

* Free software: BSD license
* Documentation: https://pyactiviti.readthedocs.org.

Features
--------

* Create/Read/Update/Delete/Search a user
* Create/Read/Update/Delete/Search a group
* List the deployments

Todo
----

* Create/Read/Update/Delete/Search Process
* Create/Read/Update/Delete/Search Instance
* Create/Read/Update/Delete/Search Task


Examples
--------

.. sourcecode:: python

    from pyactiviti import Activiti

    ACTIVITI_AUTH = ('kermit', 'kermit')
    ACTIVITI_API = 'http://localhost:8080/activiti-rest'

    activiti = Activiti(ACTIVITI_API, auth=ACTIVITI_AUTH)

    if not activiti.user_exists('user1'):
        user = activiti.create_user('user1', 'foo@bar.org', 'secret')
    else:
        user = activiti.get_user('user1')

    group = activiti.create_group('group1', 'Group1', 'Type')
    activiti.group_add_member(group['Id'], user['Id'])
