"""
dispatch RPC payloads to NetConf server.
"""
import logging

import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError
from ncclient.transport.errors import SSHError, AuthenticationError

logger = logging.getLogger(__name__)

mgr = None  # Connection Manager


def reset():
    """
    closure on appConfig to reset connection
    """


def init(config):
    """
    initialise "mgr" adding a clousre to context to re-establish connection,
    if need be...
    return True if connection to remote host is successful,
    otherwise False to fast-fail
    """
    global reset

    def reset():
        """
        closure on appConfig to reset/retry ncMgr in case of connection loss
        """
        global mgr
        mgr = None
        try:
            mgr = manager.connect(port=830, timeout=90,
                                  host=config['HOST'],
                                  username=config['USR'],
                                  password=config['PASSWD'],
                                  hostkey_verify=False, allow_agent=False,
                                  device_params={'name': 'iosxr'})
            logger.info('connected to "%s"', config['HOST'])
        except AuthenticationError as e:
            logger.error(e)
        except SSHError as e:
            logger.error(e)
        return mgr is not None
    return reset()


def dispatch(payload):
    """
    send RPC payload (sync) to NetConf server, reset connection manager on Exception
    """
    logger.debug('dispatching RPC paylad -> %s', payload)
    try:
        rsp = mgr.dispatch(et.fromstring(payload)).xml
        return True
    except RPCError as e:
        rsp = e.xml
    except SSHError as e:
        logger.error(e)
        logger.info('reconnecting to remote host ...')
        reset()
        raise e

    if et.iselement(rsp):
        rsp = et.tostring(rsp, pretty_print=True).decode()

    logger.debug('RPC response -> %s', rsp)
    return False
