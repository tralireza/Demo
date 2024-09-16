"""
dispatch RPC payloads to NetConf server.
"""
import logging

import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError
from paramiko.ssh_exception import SSHException, AuthenticationException

logger = logging.getLogger(__name__)

mgr = None  # Connection Manager


def reset():
    """
    closure on appConfig to reset connection
    """


def init(appConfig):
    """
    initialise ncMgr adding a clousre to context to re-establish connection,
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
                                  host=appConfig['HOST'],
                                  username=appConfig['USR'],
                                  password=appConfig['PASSWD'],
                                  hostkey_verify=False, allow_agent=False,
                                  device_params={'name': 'iosxr'})
            logger.info('connected to "%s"', appConfig['HOST'])
        except AuthenticationException as e:
            logger.error(e)
        except SSHException as e:
            logger.error(e)
        return mgr is not None
    return reset()


def dispatch(rpcXml):
    """
    send the rpc payload (sync), reset connection manager (ncMgr) on Exception
    """
    logger.debug('dispatching RCP paylad -> %s', rpcXml)
    try:
        rsp = mgr.dispatch(et.fromstring(rpcXml)).xml
        return True
    except RPCError as e:
        rsp = e.xml
    except SSHException as e:
        logger.error(e)
        logger.info('trying to re-connect to remote host ...')
        reset()
        raise SSHException()

    if et.iselement(rsp):
        rsp = et.tostring(rsp, pretty_print=True).decode()

    logger.debug('RPC response -> %s', rsp)
    return False
