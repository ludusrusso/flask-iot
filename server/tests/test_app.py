import pytest

def test_app_is_running(client):
    res = client.get('/')
    assert res.status_code is not None
