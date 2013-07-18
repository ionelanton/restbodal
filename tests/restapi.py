import unittest
from multiprocessing import Process
import requests
from lib.bottle import run
import json
import routes


class TestRestApi(unittest.TestCase):

    def setUp(self):
        self.p = Process(target=run_test_server)
        self.p.daemon = True
        self.p.start()

    def tearDown(self):
        self.p.terminate()

    def test_rest_api(self):
        self.can_add_a_person()
        self.cannot_add_a_person_with_incomplete_infos()
        self.can_get_all_persons()
        self.can_get_a_person_by_id()
        self.can_update_a_person_by_id()
        self.cannot_update_a_person_with_incomplete_infos()
        self.can_delete_a_person_by_id()

    def can_add_a_person(self):

        person = json.dumps({u'firstname': u'Johnny', u'lastname': u'Mnemonic', u'gender': u'M', u'phone': u'111-222-3333'})
        r = requests.post('http://localhost:' + TestPort.string + '/persons',
                          data=person,
                          headers={'content-type': 'application/json'})

        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['result'], 'success', 'Cannot add person')

    def cannot_add_a_person_with_incomplete_infos(self):

        person = json.dumps({u'firstname': u'', u'lastname': u'', u'gender': u'', u'phone': u''})
        r = requests.post('http://localhost:' + TestPort.string + '/persons',
                          data=person,
                          headers={'content-type': 'application/json'})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['result'], 'error', 'Can add a person with incomplete infos')
        self.assertEqual(r.json()['message']['firstname'], 'firstname cannot be empty')
        self.assertEqual(r.json()['message']['lastname'], 'lastname cannot be empty')
        self.assertEqual(r.json()['message']['gender'], 'value not allowed')

    def can_get_all_persons(self):
        person = json.dumps({u'firstname': u'Robo', u'lastname': u'Cop', u'gender': u'M', u'phone': u''})
        r = requests.post('http://localhost:' + TestPort.string + '/persons',
                          data=person,
                          headers={'content-type': 'application/json'})

        r = requests.get('http://localhost:' + TestPort.string + '/persons')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2, "Cannot get all the persons")

    def can_get_a_person_by_id(self):
        r = requests.get('http://localhost:' + TestPort.string + '/persons/1')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['id'], 1, "Cannot get the person at /persons/1")

    def can_update_a_person_by_id(self):
        person = json.dumps({u'firstname': u'Johnny2', u'lastname': u'Mnemonic2', u'gender': 'M', u'phone': ''})

        r = requests.put('http://localhost:' + TestPort.string + '/persons/1',
                         data=person, headers={'content-type': 'application/json'})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['result'], 'success', "Cannot update the person at /persons/1")

    def cannot_update_a_person_with_incomplete_infos(self):
        person = json.dumps({u'firstname': u'', u'lastname': u'', u'gender': '', u'phone': ''})

        r = requests.put('http://localhost:' + TestPort.string + '/persons/1',
                         data=person, headers={'content-type': 'application/json'})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['result'], 'error', "Can update a person with incomplete infos")
        self.assertEqual(r.json()['message']['firstname'], 'firstname cannot be empty')
        self.assertEqual(r.json()['message']['lastname'], 'lastname cannot be empty')
        self.assertEqual(r.json()['message']['gender'], 'value not allowed')

    def can_delete_a_person_by_id(self):
        r = requests.delete('http://localhost:' + TestPort.string + '/persons/2')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['result'], 'success', 'Cannot delete person')
        self.assertEqual(r.json()['message'], 'Person deleted')


class TestPort:
    value = 8088
    string = str(value)


def run_test_server():
    reload(routes)
    run(host='localhost', port=TestPort.value, quiet=True)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRestApi))
    return suite

TestRestApiSuite = suite()
