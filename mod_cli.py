import logging

from flask import Blueprint
from netmiko import ConnectHandler


bp = Blueprint('cli', __name__, url_prefix='/cli')
logger = logging.getLogger(__name__)
mgr, reset = None, None


def init(appConfig):
    global mgr

    def reset():
        """
        closure on appConfig to reset connecting in case of connection loss
        """
        global mgr

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


@bp.get('/ifs')
def ifs():
    try:
        return mgr.send_command('show interfaces brief'), 200

    except Exception as e:
        logger.error(e)
        reset()

    return '', 500


@bp.get('/version')
def version():
    try:
        return mgr.send_command('show version'), 200

    except Exception as e:
        logger.error(e)
        reset()

    return '', 500
