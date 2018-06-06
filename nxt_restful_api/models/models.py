# -*- coding: utf-8 -*-

import odoo
from odoo import models, fields, api
from odoo.addons.iap.models.iap import jsonrpc, InsufficientCreditError


DEFAULT_ENDPOINT = 'http://iap-service.y11c.appnxt.com'
class nxt_restful_api(models.Model):
    _name = 'nxt.api'

    @api.model
    def get_token(self, serv=None, login=None, password='admin', db='odoo'):
        user_token = self.env['iap.account'].get('nxt_restful_api')
        params = {
            'account_token': user_token.account_token,
            'kw':{
                'serv': serv,
                'login': login,
                'password': password,
                'db': db,
            }
        }
        endpoint = self.env['ir.config_parameter'].sudo().get_param('nxt_restful_api.endpoint', DEFAULT_ENDPOINT)
        return jsonrpc(endpoint + '/odoo/token', params=params)

    @api.model
    def get(self,model,ids,kw):
        user_token = self.env['iap.account'].get('nxt_restful_api')
        endpoint = self.env['ir.config_parameter'].sudo().get_param('nxt_restful_api.endpoint', DEFAULT_ENDPOINT)
        params = {
            'account_token': user_token.account_token,
            'model': model,
            'ids': ids,
            'kw': kw
        }
        return jsonrpc(endpoint +'/odoo/get',params=params)

    @api.model
    def post(self,model,kw):
        user_token = self.env['iap.account'].get('nxt_restful_api')
        endpoint = self.env['ir.config_parameter'].sudo().get_param('nxt_restful_api.endpoint', DEFAULT_ENDPOINT)
        params = {
            'account_token': user_token.account_token,
            'model': model,
            'kw': kw
        }
        return jsonrpc(endpoint +'/odoo/post',params=params)
    @api.model
    def delete(self,model,ids,kw):
        user_token = self.env['iap.account'].get('nxt_restful_api')
        endpoint = self.env['ir.config_parameter'].sudo().get_param('nxt_restful_api.endpoint', DEFAULT_ENDPOINT)
        params = {
            'account_token': user_token.account_token,
            'model': model,
            'ids':ids,
            'kw': kw
        }
        return jsonrpc(endpoint +'/odoo/delete',params=params)
    @api.model
    def put(self,model,ids,kw):
        user_token = self.env['iap.account'].get('nxt_restful_api')
        endpoint = self.env['ir.config_parameter'].sudo().get_param('nxt_restful_api.endpoint', DEFAULT_ENDPOINT)
        params = {
            'account_token': user_token.account_token,
            'model': model,
            'ids':ids,
            'kw': kw
        }
        return jsonrpc(endpoint +'/odoo/put',params=params)
    @api.model
    def call_method(self,model,method,args,kwargs):
        user_token = self.env['iap.account'].get('nxt_restful_api')
        endpoint = self.env['ir.config_parameter'].sudo().get_param('nxt_restful_api.endpoint', DEFAULT_ENDPOINT)
        params = {
            'account_token': user_token.account_token,
            'model': model,
            'method': method,
            'args': args,
            'kw': kwargs
        }
        return jsonrpc(endpoint +'/odoo/call_method',params=params)