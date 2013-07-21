from model.db import db
from lib.bottle import route, response, request, static_file
import json


@route('/')
def index():
    return static_file('index.html', root='web')


@route('/web/<filepath:path>')
def static(filepath):
    return static_file(filepath, root='web')


@route('/sammy/<filepath:path>')
def web_client_sammy(filepath):
    return static_file(filepath, root='web/clients/sammy')


@route('/persons', method='POST')
def add_person():
    response.content_type = AppConfig.content_type

    person = request.json
    record = db.person.validate_and_insert(
        firstname=person['firstname'],
        lastname=person['lastname'],
        gender=person['gender'],
        phone=person['phone'])
    if not record.errors:
        db.commit()
        response.status = 201
        return str(json.dumps({u'result': u'success', u'message': u'Added person into database'}))
    else:
        return str(json.dumps({u'result': u'error', u'message': record.errors.as_dict()}))


@route('/persons', method='GET')
def all_persons():
    response.content_type = AppConfig.content_type
    return json.dumps(db().select(db.person.ALL).as_list())


@route('/persons/:id')
def get_person(id):
    response.content_type = AppConfig.content_type
    person = db(db.person.id == id).select(db.person.ALL).first()
    if person:
        return str(json.dumps(person.as_dict()))
    else:
        return str(json.dumps(dict()))


@route('/persons/:id', 'PUT')
def update_person(id):
    response.content_type = AppConfig.content_type
    person = request.json
    record = db(db.person.id == id).validate_and_update(
        firstname=person['firstname'],
        lastname=person['lastname'],
        gender=person['gender'],
        phone=person['phone']
    )

    if not record.errors:
        db.commit()
        return str(json.dumps({u'result': u'success', u'message': u'Updated person into database'}))
    else:
        return str(json.dumps({u'result': u'error', u'message': record.errors.as_dict()}))


@route('/persons/:id', 'DELETE')
def delete_person(id):
    response.content_type = AppConfig.content_type
    n = db(db.person.id == id).delete()

    if n == 1:
        db.commit()
        return str(json.dumps({u'result': u'success', u'message': u'Person deleted'}))
    else:
        return str(json.dumps({u'result': u'error', u'message': u'Person does not exists'}))


class AppConfig:
    content_type = 'application/json; charset=UTF-8'
