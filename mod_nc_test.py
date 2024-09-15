import logging

import pytest

import env
import mod_nc as m


m.logger.setLevel(logging.DEBUG)


@pytest.fixture
def dispatcher():
    import dispatcher
    dispatcher.logger.setLevel(logging.DEBUG)
    dispatcher.init(env.appConfig)
    yield dispatcher


def test_lifCreate(dispatcher):
    class MyReq:
        def get_json(self):
            return {'number': 8118,
                    'addr': '10.0.0.1',
                    'mask': '255.255.255.0',
                    }

    m.state.dryrun = True
    m.request = MyReq()
    rpcXml, status = m.lifCreate()

    print(rpcXml)

    assert 'Loopback8118' in rpcXml
    assert 200 == status

    assert 'message-id="2"' in m.lifCreate()[0]
    assert 'message-id="3"' in m.lifCreate()[0]

    m.state.dryrun = False
    print(m.lifCreate())


def test_lifDelete(dispatcher):
    m.state.dryrun = True
    assert 'Loopback8118' in m.lifDelete(8118)[0]

    m.state.dryrun = False
    m.dispatcher = dispatcher
    print(m.lifDelete(8118))
