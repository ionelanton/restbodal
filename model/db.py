from lib.web2py.dal import *
from lib.web2py.validators import *

db = DAL('sqlite:memory')
#db = DAL('postgres://username:password@localhost/database')

db.define_table('person',
                Field('firstname', 'string', length=100, requires=IS_NOT_EMPTY(error_message='firstname cannot be empty')),
                Field('lastname', 'string', length=100, requires=IS_NOT_EMPTY(error_message='lastname cannot be empty')),
                Field('gender', 'string', length=1, requires=IS_IN_SET(['M', 'F'])),
                Field('phone', 'string', length=15)
                )

