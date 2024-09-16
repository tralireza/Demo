import json
import logging

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

import env
import mod_nc as nc
import mod_cli as cli


logging.basicConfig(format='%(asctime)s|%(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info('starting...')

app = Flask(__name__, static_folder=None)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.register_blueprint(nc.bp)
app.register_blueprint(cli.bp)

appConfig = env.appConfig

if not nc.dispatcher.init(appConfig):
    logger.critical('[NetConf] no connection possible: %s' % appConfig)
    exit(-1)

if not cli.init(appConfig):
    logger.critical('[Cli] no connection possible: %s' % appConfig)
    exit(-1)


@app.get('/config')
def config():
    return json.dumps(appConfig, indent=2)


@app.get('/alive')
def alive():
    return json.dumps({"alive": True}, indent=2)


@app.get('/dryrun')
def dryrun():
    nc.state.dryrun = not nc.state.dryrun
    return json.dumps({"dryrun": nc.state.dryrun}, indent=2)


logger.info('ready...')
