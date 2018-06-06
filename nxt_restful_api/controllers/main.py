#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : main.py
# @Time    : 2018/6/6 下午6:14
# @Author  : JackCao
# @Email   : 63720750@qq.com
# @Site    : http://appnxt.com

from functools import wraps
import json

from odoo.tools.safe_eval import safe_eval
from odoo.http import Controller, request, route

class make_response():

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = decode_bytes(func(*args, **kwargs))
                return request.make_response(json.dumps(result))
            except Exception as e:
                return request.make_response(json.dumps({'error': str(e)}))
        return wrapper


def eval_request_params(kwargs):
    for k, v in kwargs.items():
        try:
            kwargs[k] = safe_eval(v)
        except:
            continue


def decode_bytes(result):
    if isinstance(result, (list, tuple)):
        decoded_result = []
        for item in result:
            decoded_result.append(decode_bytes(item))
        return decoded_result
    if isinstance(result, dict):
        decoded_result = {}
        for k, v in result.items():
            decoded_result[decode_bytes(k)] = decode_bytes(v)
        return decoded_result
    if isinstance(result, bytes):
        return result.decode('utf-8')
    return result


class RestApi(Controller):
    """
    /api/v2/auth                   POST    - Login in Odoo and set cookies

    /api/v2/<model>                GET     - Read all (with optional domain, fields, offset, limit, order)
    /api/v2/<model>/<id>           GET     - Read one (with optional fields)
    /api/v2/<model>                POST    - Create one
    /api/v2/<model>/<id>           PUT     - Update one
    /api/v2/<model>/<id>           DELETE  - Delete one
    /api/v2/<model>/<id>/<method>  PUT     - Call method (with optional parameters)
    """

    @route('/api/v2/auth', auth='none', methods=["POST"])
    @make_response()
    def authenticate(self, db, login, password):
        # Before calling /api/v2/auth, call /web?db=*** otherwise web service is not found
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @route('/api/v2/<string:model>', auth='user', methods=["GET"])
    @make_response()
    def search_read(self, model, **kwargs):
        eval_request_params(kwargs)
        return request.env[model].search_read(**kwargs)

    @route('/api/v2/<string:model>/<int:id>', auth='user', methods=["GET"])
    @make_response()
    def read(self, model, id, **kwargs):
        eval_request_params(kwargs)
        result = request.env[model].browse(id).read(**kwargs)
        return result and result[0] or {}

    @route('/api/v2/<string:model>', auth='user',
           methods=["POST"], csrf=False)
    @make_response()
    def create(self, model, **kwargs):
        eval_request_params(kwargs)
        return request.env[model].create(**kwargs).id

    @route('/api/v2/<string:model>/<int:id>', auth='user',
           methods=["PUT"], csrf=False)
    @make_response()
    def write(self, model, id, **kwargs):
        eval_request_params(kwargs)
        return request.env[model].browse(id).write(**kwargs)

    @route('/api/v2/<string:model>/<int:id>', auth='user',
           methods=["DELETE"], csrf=False)
    @make_response()
    def unlink(self, model, id):
        return request.env[model].browse(id).unlink()

    @route('/api/v2/<string:model>/<int:id>/<string:method>', auth='user',
           methods=["PUT"], csrf=False)
    @make_response()
    def custom_method(self, model, id, method, **kwargs):
        eval_request_params(kwargs)
        record = request.env[model].browse(id)
        return getattr(record, method)(**kwargs)