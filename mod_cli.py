"""
in charge of CLI conversation with a Cisco IOS device.
Keeps connection open and retry if it drops.
"""
import logging

from flask import Blueprint
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException, AuthenticationException


bp = Blueprint('cli', __name__, url_prefix='/cli')
logger = logging.getLogger(__name__)
mgr = None


def reset():
    """
    closure to retry connection loss
    """


def init(appConfig):
    """
    initialize the connection and update the closure reset() for retry later
    """
    global reset

    def reset():
        """
        closure on appConfig to reset connecting in case of connection loss
        """
        global mgr
        if mgr:
            try:
                mgr.disconnect()
            except SSHException:
                pass
        mgr = None
        try:
            mgr = ConnectHandler(port=22,
                                 host=appConfig['HOST'],
                                 username=appConfig['USR'],
                                 password=appConfig['PASSWD'],
                                 device_type='cisco_ios')
            logger.info('conntected to "%s"', appConfig['HOST'])
        except AuthenticationException as e:
            logger.error(e)
        except SSHException as e:
            logger.error(e)
        return mgr is not None
    return reset()


@bp.get('/ifs')  # ifs as interfaces (including Loopback)
def ifs():
    """
    return output of "show interfaces brief"
    """
    try:
        return mgr.send_command('show interfaces brief'), 200, {'Content-Type': 'text/plain'}
    except SSHException as e:
        logger.error(e)
        reset()
    return '', 504


@bp.get('/version')
def version():
    """
    return output of "show version"
    """
    try:
        return mgr.send_command('show version'), 200, {'Content-Type': 'text/plain'}
    except SSHException as e:
        logger.error(e)
        reset()
    return '', 504
