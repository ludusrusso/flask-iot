import pytest
from .. import create_app, db as _db
import json
from flask import Response as BaseResponse, url_for as _url_for
from flask.testing import FlaskClient
from werkzeug.utils import cached_property
from ..models import User

class Response(BaseResponse):
    @cached_property
    def json(self):
        return json.loads(self.data)


class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return super(TestClient, self).open(*args, **kwargs)


@pytest.fixture
def app(request):
    app = create_app()
    app.debug = True
    app.test = True
    app.config['SECRET_KEY'] = 'secret'

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def client(app):
    app.response_class = Response
    app.test_client_class = TestClient
    return app.test_client()

@pytest.fixture
def db(app, request):
    _db.app = app
    _db.create_all()
    def teardown():
        _db.drop_all()
    request.addfinalizer(teardown)
    return _db

@pytest.fixture
def password():
    return 'password'


@pytest.fixture
def user(app, password, db):
    user = User(username='test', email='email', password=password)
    db.session.add(user)
    db.session.commit()
    return user
