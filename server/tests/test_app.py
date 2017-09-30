import pytest
from flask import url_for
from .. import api_v1

def test_app_is_running(client):
    res = client.get('/')
    assert res.status_code is not None

def test_json_response(client, app):
    res = client.get('/', json={})
    assert res.content_type == 'application/json'
    assert isinstance(res.json, dict)
    assert 'apis' in res.json.keys()
    with app.test_request_context('/'):
        assert url_for("api_v1.base") in res.json['apis']
