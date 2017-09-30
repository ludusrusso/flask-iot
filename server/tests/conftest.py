import pytest
from .. import create_app

@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    app.test = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()
