import logging

import pytest

import env
import dispatcher as m


m.logger.setLevel(logging.DEBUG)


@pytest.fixture()
def appConfig():
    appConfig = env.appConfig
    yield appConfig


def test_connect(appConfig):
    host = appConfig['HOST']

    appConfig['HOST'] = '127.0.0.1'
    assert m.init(appConfig) is False

    appConfig['HOST'] = host
    assert m.init(appConfig) is True


def test_dispatch(appConfig):
    m.init(appConfig)
    assert m.dispatch('''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="%i">
  <target>
    <candidate/>
  </target>
  <config>
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-interface-cfg">
      <interface>
        <interface-name>Loopback%i</interface-name>
      </interface>
    </interfaces>
  </config>
</edit-config>''' % (1001, 9191)) is True


def test_reconnect():
    try:
        m.mgr.close_session()
    except Exception as e:
        print(e)

    try:
        m.dispatch('''<commit xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1001" />''') is False
        assert False
    except Exception as e:
        print("->", type(e).__name__, "::", e)
        assert True
