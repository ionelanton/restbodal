import unittest
from tests.web2py import *
from tests.restapi import *

runner = unittest.TextTestRunner()
runner.run(TestWeb2pySuite)
runner.run(TestRestApiSuite)