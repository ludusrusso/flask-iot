import pytest
from flask import url_for, request
from .. import api_v1

from ..decorators import expected_body, expected_args
from voluptuous import Required, Schema, MultipleInvalid, Invalid
from ..models import User

def test_app_is_running(client):
    res = client.get('/')
    assert res.status_code is not None

def test_login_required(client):
    res = client.get('/')
    assert res.status_code == 401 # unauthorized
    assert res.headers['Location'] == url_for('token.request_token')


def test_json_response(client, app):
    res = client.get('/', json={})
    assert res.content_type == 'application/json'
    assert isinstance(res.json, dict)
    assert 'v1' in res.json.keys()

def test_api_v1_catalog(app):
    with app.test_request_context():
        catalog = api_v1.get_catalog()
        assert 'device' in catalog.keys()
        assert 'user' in catalog.keys()
        assert isinstance(catalog['device'], list)
        assert isinstance(catalog['user'], list)

def test_expected_decorator(app, client):

    schema = Schema({
        Required('text'): str,
        Required('per_page', default=5): int
    })

    @expected_body(schema, 'body')
    def func(body):
        assert body['text'] == 'testo'
        assert body['per_page'] == 5

    with app.test_request_context():
        ret = func()
        ret.status_code = 406

    with app.test_request_context(method='POST', data={'text': 'testo'}):
        ret = func()

def test_expected_args_decorator(app, client):

    schema = Schema({
        Required('text'): str,
        Required('per_page', default=5): int
    })

    @expected_args(schema, 'args')
    def func(args):
        assert args['text'] == 'testo'
        assert args['per_page'] == 5

    with app.test_request_context():
        ret = func()
        ret.status_code = 406

    with app.test_request_context('?text=testo', method='GET'):
        ret = func()

def test_login(app, user, client, password):
    payload = {'username': user.username, 'password': password}
    with app.test_request_context():
        res = client.post(url_for('api_v1.login'), json=payload)
        print(res.json)

    assert res.status_code == 200
    assert 'token' in res.json
    assert user.id == User.query_with_token(res.json['token']).id

def test_login_err(app, user, client, password):
    payload = {'username': user.username, 'password': password + 'asd'}
    with app.test_request_context():
        res = client.post(url_for('api_v1.login'), json=payload)

    assert res.status_code == 401
    assert 'token' not in res.json
