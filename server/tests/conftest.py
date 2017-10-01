import pytest
from .. import create_app
import json
from flask import Response as BaseResponse
from flask.testing import FlaskClient
from werkzeug.utils import cached_property

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
def app():
    app = create_app()
    app.debug = True
    app.test = True
    return app

@pytest.fixture
def client(app):
    app.response_class = Response
    app.test_client_class = TestClient
    return app.test_client()
