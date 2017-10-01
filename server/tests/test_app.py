import pytest
from flask import url_for
from .. import api_v1


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
