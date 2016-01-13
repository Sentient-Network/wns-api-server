#!/usr/bin/env python

from flask import Flask, Response
import netki.api.domain
from netki.util.logutil import LogUtil

# Get Config
from netki.common.config import ConfigManager
config = ConfigManager().get_config()

# Setup Logging
log = LogUtil.setup_logging('netki_wns_api_server')

# Setup Flask App
app = Flask(__name__)
app.config.update(
    DEBUG=False,
    TESTING=False
)

# ###########################################
# Monitoring Testing Route
# ###########################################
@app.route('/index.html', methods=['GET', 'OPTIONS', 'HEAD', 'POST'])
def index():
    return Response("UP", status=200, mimetype='text/html')

@app.route('/api/wallet_lookup/<wallet_name>/<currency>', methods=['GET'])
def wallet_lookup(wallet_name, currency):
    return netki.api.domain.api_wallet_lookup(wallet_name, currency)

@app.route('/api/wallet_lookup/<wallet_name>/available_currencies', methods=['GET'])
def currency_lookup(wallet_name):
    return netki.api.domain.walletname_currency_lookup(wallet_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)