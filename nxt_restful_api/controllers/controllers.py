# -*- coding: utf-8 -*-
# author: 63720750@qq.com
# website: http://appnxt.com

# -*- coding: utf-8 -*-

import json
from functools import wraps
from odoo.tools.safe_eval import safe_eval
from odoo.http import Controller, request, route
from odoo.models import BaseModel

def eval_request_params(kwargs):
    for k, v in kwargs.iteritems():
        try:
            kwargs[k] = safe_eval(v)
        except:
            continue

def make_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, BaseModel):
                result = result.ids
            return request.make_response(json.dumps(result))
        except Exception, e:
            return request.make_response(json.dumps({'error': str(e)}))
    return wrapper

class RestApi(Controller):
    @route('/api/v2/auth', auth='none', methods=["POST","GET"],csrf=False)
    @make_response
    def authenticate(self, db, login, password):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @route('/api/v2/<string:model>', auth='user', methods=["GET"])
    @make_response
    def search_read(self, model, **kwargs):
        eval_request_params(kwargs)
        return request.env[model].search_read(**kwargs)

    @route('/api/v2/<string:model>/<int:id>', auth='user', methods=["GET"])
    @make_response
    def read(self, model, id, **kwargs):
        eval_request_params(kwargs)
        result = request.env[model].browse(id).read(**kwargs)
        return result and result[0] or {}

    @route('/api/v2/<string:model>', auth='user', methods=["POST"], csrf=False)
    @make_response
    def create(self, model, **kwargs):
        eval_request_params(kwargs)
        return request.env[model].create(**kwargs).id

    @route('/api/v2/<string:model>/<int:id>', auth='user', methods=["PUT"], csrf=False)
    @make_response
    def write(self, model, id, **kwargs):
        eval_request_params(kwargs)
        return request.env[model].browse(id).write(**kwargs)

    @route('/api/v2/<string:model>/<int:id>', auth='user', methods=["DELETE"], csrf=False)
    @make_response
    def unlink(self, model, id):
        return request.env[model].browse(id).unlink()

    @route('/api/v2/<string:model>/<int:id>/<string:method>', auth='user', methods=["PUT","POST"], csrf=False)
    @make_response
    def custom_method(self, model, id, method, **kwargs):
        eval_request_params(kwargs)
        record = request.env[model].browse(id)
        return getattr(record, method)(**kwargs)
