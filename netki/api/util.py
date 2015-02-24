__author__ = 'mdavid'

import json
from urlparse import urlparse

from flask import Response, request, current_app

from netki.util.logutil import LogUtil

log = LogUtil.setup_logging('util_api')

def create_json_response(success=True, message='', status=200, data={}):
    
    allowed_origins = ['localhost', '127.0.0.1']

    # Generate Allowed Origins
    origin_value = None
    for origin in allowed_origins:
        if request.referrer and origin in request.referrer:
            try:
                _uri = urlparse(request.referrer)
                origin_value = '%s://%s' % (_uri.scheme, _uri.netloc)
                break
            except:
                pass

    # This is a last-ditch effort
    if not origin_value:
        origin_value = '*'

    # Generate Allowed Methods
    _app = current_app._get_current_object()
    allow_methods = set()
    for rule in _app.url_map._rules:
        if rule.rule == request.url_rule.rule:
            allow_methods.update(rule.methods)
    
    default_headers = {
        'Access-Control-Allow-Origin': origin_value,
        'Access-Control-Allow-Methods': ', '.join(allow_methods),
        'Access-Control-Allow-Headers': 'X-Requested-With, accept, content-type'
    }

    rdict = {}
    rdict['success'] = success
    rdict['message'] = message
    for key in data.keys():
        if key not in ['success', 'message']:
            rdict[key] = data[key]

    # Certain response codes don't contain data
    if status in [204]:
        return Response(None, status=status, mimetype='application/json', headers=default_headers)

    return Response(json.dumps(rdict), status=status, mimetype='application/json', headers=default_headers)