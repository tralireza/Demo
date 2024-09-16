import logging

import pytest

from app import app as Work


logging.basicConfig(level=logging.DEBUG)


@pytest.fixture()
def app():
    Work.config.update({"TESTING": True})
    yield Work


@pytest.fixture()
def client(app):
    return app.test_client()


def test_alive(client):
    rsp = client.get('/alive')
    assert 200 == rsp.status_code
    assert b'true' in rsp.data


def test_config(client):
    print(client.get('/config'))


def test_dryrun(client):
    rsp = client.get('/dryrun')
    assert b'true' in rsp.data

    rsp = client.get('/dryrun')
    assert b'false' in rsp.data
