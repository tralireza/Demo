import logging

from flask import Blueprint
from netmiko import ConnectHandler


bp = Blueprint('cli', __name__, url_prefix='/cli')
logger = logging.getLogger(__name__)
mgr, reset = None, None


def init(appConfig):
    global reset

    def reset():
        """
        closure on appConfig to reset connecting in case of connection loss
        """
        global mgr
        if mgr:
            try:
                mgr.disconnect()
            except Exception:
                pass
        mgr = None
        try:
            mgr = ConnectHandler(port=22,
                                 host=appConfig['HOST'],
                                 username=appConfig['USR'],
                                 password=appConfig['PASSWD'],
                                 device_type='cisco_ios')
            logger.info('conntected to "%s"' % appConfig['HOST'])
        except Exception as e:
            logger.error(e)
        return mgr is not None
    return reset()


@bp.get('/ifs')  # ifs as interfaces (including Loopback)
def ifs():
    try:
        return mgr.send_command('show interfaces brief'), 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        logger.error(e)
        reset()
    return '', 504


@bp.get('/version')
def version():
    try:
        return mgr.send_command('show version'), 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        logger.error(e)
        reset()
    return '', 504
