"""
NetConf module
"""
import logging

from flask import Blueprint, request
from paramiko.ssh_exception import SSHException

import dispatcher
from rpc_payload_cisco import (Payload, IF_CREATE, IF_DEL, COMMIT)


class State:
    """
    this module's state
    dryrun: return early without calling dispatcher
    seq: number of RPCs sent via dispatcher
    """
    def __init__(self, seq=0, dryrun=True):
        self.seq, self.dryrun = seq, dryrun

    def inc(self):
        """ mutate sequence """
        self.seq += 1
        return self.seq


bp = Blueprint('nc', __name__, url_prefix='/netconf')
logger = logging.getLogger(__name__)
state = State()


@bp.post('/lfs')  # lfs as Loopback interfaces
def lif_create():
    """
    create a Loopback interface with a number provided in POST json request
    """
    jdata = request.get_json()
    number = jdata['number']

    rpcXml = Payload[IF_CREATE] % (state.inc(), f'Loopback{number}')
    if state.dryrun:
        return rpcXml, 200

    logger.debug(rpcXml)

    try:
        if dispatcher.dispatch(rpcXml):
            rpcXml = Payload[COMMIT] % state.inc()
            if dispatcher.dispatch(rpcXml):
                return '', 200
        return '', 400
    except SSHException as e:
        logger.error(e)
    return '', 500


@bp.route('/lfs/<int:number>', methods=['DELETE'])
def lif_delete(number):
    """
    delete a loopback inteface
    """
    rpcXml = Payload[IF_DEL] % (state.inc(), f'Loopback{number}')
    if state.dryrun:
        return rpcXml, 200

    logger.debug(rpcXml)

    try:
        if dispatcher.dispatch(rpcXml):
            rpcXml = Payload[COMMIT] % state.inc()
            if dispatcher.dispatch(rpcXml):
                return '', 200
        return '', 400
    except SSHException as e:
        logger.error(e)
    return '', 400
