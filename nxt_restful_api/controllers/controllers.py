# -*- coding: utf-8 -*-
# author: 63720750@qq.com
# website: http://appnxt.com

import odoo
from odoo import api, http, SUPERUSER_ID, _
from odoo.http import request
import werkzeug
import base64
import time
import json
import logging
import pdb

_logger = logging.getLogger(__name__)


###############################
#
# Odoo Nxt Restful API Method.
#
###############################

def no_token():
    rp = {'result': '','success': False,'message':'invalid token!'}
    return json_response(rp)

def json_response(rp):
    headers = {"Access-Control-Allow-Origin": "*"}
    return werkzeug.wrappers.Response(json.dumps(rp,ensure_ascii=False), mimetype='application/json',headers=headers)

db = 'v11c-iap'
cr = odoo.registry(db).cursor()
env = api.Environment(cr, SUPERUSER_ID, {})

class NxtRestfulApi(http.Controller):
    @http.route([
        '/api/v1/get_token',
        ], type='http', auth="none", csrf=False, methods=['POST','GET'])
    def token(self, login=None, password='admin', db='odoo'):
        rp = env['nxt.api'].get_token(request.httprequest.host_url,login,password,db)
        return json_response(rp)

    @http.route([
        '/api/v1/<string:model>',
        '/api/v1/<string:model>/<string:ids>'
        ], auth='none', type='http', csrf=False, methods=['GET'])
    def read_objects(self, model=None, ids=None, **kw):
        rp = env['nxt.api'].get(model,ids,kw)
        return json_response(rp)

    @http.route([
        '/api/v1/<string:model>',
        ], auth='none', type='http', csrf=False, methods=['POST'])
    def create_objects(self, model=None, **kw):
        rp = env['nxt.api'].post(model,kw)
        return json_response(rp)

    @http.route([
        '/api/v1/<string:model>/<string:ids>',
        ], auth='none', type='http', csrf=False, methods=['PUT','PATCH'])
    def update_objects(self, model=None, ids=None, **kw):
        rp = env['nxt.api'].put(model,ids,kw)
        return json_response(rp)

    @http.route([
        '/api/v1/<string:model>/<string:ids>',
        ], auth='none', type='http', csrf=False, methods=['DELETE'])
    def unlink_objects(self, model=None, ids=None, **kw):
        rp = env['nxt.api'].delete(model, ids,kw)
        return json_response(rp)

    @http.route([
        '/api/v1/<string:model>/call/<string:method>/<string:args>',
        ], auth='none', type='http', csrf=False, methods=['POST','GET'])
    def call_method(self, model=None, method=None,args='', **kw):
        rp = env['nxt.api'].call_method(model, method,eval(args),kw)
        return json_response(rp)
