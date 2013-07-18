from lib.bottle import run
import routes

run(host='localhost', port=8080, debug=True)

# # print db.tables
# # print db.friend.fields
#
# ret = db.friend.validate_and_insert(name='', surname='')
#
# print ret.errors
#
# for e in ret.errors:
#     print e + ': ' + ret.errors[e]
#
# if not ret.errors:
#     for row in db().select(db.friend.name, orderby=db.friend.name):
#         print row.name + ', ' + row.surname
# else:
#     print 'errors...'
