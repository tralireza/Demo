"""
NetConf module
"""

import dataclasses
import logging

from flask import Blueprint, request
from paramiko.ssh_exception import SSHException

import dispatcher
from rpc_payload_cisco import (Payload, IF_CREATE, IF_DEL, COMMIT)


@dataclasses.dataclass
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

    payload = Payload[IF_CREATE] % (state.inc(), f'Loopback{number}')
    if state.dryrun:
        return payload, 200, {"content-type": "text/xml"}

    logger.debug(payload)

    try:
        if dispatcher.dispatch(payload):
            payload = Payload[COMMIT] % state.inc()
            if dispatcher.dispatch(payload):
                return '', 200
        return '', 400
    except (SSHException, Exception):
        return '', 504


@bp.route('/lfs/<int:number>', methods=['DELETE'])
def lif_delete(number):
    """
    delete a loopback inteface
    """
    payload = Payload[IF_DEL] % (state.inc(), f'Loopback{number}')
    if state.dryrun:
        return payload, 200, {"content-type": "text/xml"}

    logger.debug(payload)

    try:
        if dispatcher.dispatch(payload):
            payload = Payload[COMMIT] % state.inc()
            if dispatcher.dispatch(payload):
                return '', 200
        return '', 400
    except (SSHException, Exception):
        return '', 504
