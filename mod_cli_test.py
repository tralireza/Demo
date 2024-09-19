import logging

import env
import mod_cli as m


m.logger.setLevel(logging.DEBUG)


def test_connect():
    assert m.init(env.appConfig) is True


def test_ifs():
    rsp, status, _ = m.ifs()
    print(rsp)

    assert status == 200


def test_version():
    rsp, status, _ = m.version()
    print(rsp)

    assert 'Cisco IOS XR' in rsp
    assert status == 200


def test_reconnect():
    try:
        m.mgr.disconnect()
    except Exception as e:
        print(e)

    _, status = m.version()
    assert status == 504
    _, status, _ = m.version()
    assert status == 200
