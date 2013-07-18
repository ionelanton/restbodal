import unittest
from lib.web2py.dal import *
from lib.web2py.validators import *
from model.db import db


class TestWeb2py(unittest.TestCase):

    def setUp(self):
        self.test_table = db.define_table('test', Field('test', requires=IS_NOT_EMPTY(error_message='Empty not allowed')))

    def tearDown(self):
        db['test'].drop()
        db.commit()

    def test_web2py_dal_can_create_table(self):
        self.assertEqual('test', str(self.test_table), "Web2py DAL cannot create table")

    def test_web2py_dal_can_validate_field_content(self):
        response = db.test.validate_and_insert(test='')
        db.commit()
        self.assertNotEqual(0, len(response.errors.as_dict()), "Web2py DAL cannot validate field content")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWeb2py))
    return suite

TestWeb2pySuite = suite()
