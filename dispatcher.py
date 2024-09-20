"""
dispatch RPC payloads to NetConf server.
"""
import logging

import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError
from ncclient.transport.errors import SSHError, AuthenticationError, TransportError

logger = logging.getLogger(__name__)

mgr = None  # Connection Manager


def reset():
    """
    closure on appConfig to reset connection
    """


def init(config):
    """
    initialise "mgr" adding a closure to context to re-establish connection,
    if need be...
    return True if connection to remote host is successful,
    otherwise False to fast-fail
    """
    global reset

    def reset():
        """
        closure on appConfig to reset/retry "mgr" in case of connection loss
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
            logger.info('(nc) connected to "%s"', config['HOST'])
        except (AuthenticationError, SSHError, TransportError) as e:
            logger.debug(e)
        return mgr is not None
    return reset()


def dispatch(payload):
    """
    send RPC payload (sync) to NetConf server, reset connection manager on Exception
    """
    logger.debug('dispatching RPC payload -> %s', payload)
    try:
        rsp = mgr.dispatch(et.fromstring(payload)).xml
        return True
    except RPCError as e:
        rsp = e.xml
    except (SSHError, TransportError) as e:
        logger.debug(e)
        logger.info('reconnecting to remote host ...')
        reset()
        raise e

    if et.iselement(rsp):
        rsp = et.tostring(rsp, pretty_print=True).decode()

    logger.debug('got RPC response <- %s', rsp)
    return False
