from ..auth import login_required, login_required_response
from flask import make_response, url_for, g
import json
import pytest

def test_login_required(app, user):

    @login_required
    def func():
        return 'current_user: %s'%g.current_user.id


    func = login_required(lambda : make_response())

    with app.test_request_context():
        res = func()

        assert res.status_code == 401
        assert res.headers['location'] == url_for('api_v1.login')

    with app.test_request_context(headers = {'authentication': 'baerer'}):
        res = func()
        assert res.status_code == 401
        assert res.headers['location'] == url_for('api_v1.login')
        with pytest.raises(AttributeError):
            g.current_user

    headers = {"authentication": "baerer " + str(user.generate_auth_token().decode(encoding='UTF-8'))}
    with app.test_request_context(headers = headers):
        res = func()
        assert res.status_code == 200
        assert g.current_user is user

def test_login_required_resposense(app):
    with app.test_request_context():
        res = login_required_response()
        assert res.status_code == 401
        assert res.headers['location'] == url_for('api_v1.login')
