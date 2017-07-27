# -*- coding: utf-8 -*-
# author: 63720750@qq.com
# website: http://appnxt.com

from odoo import api, http, SUPERUSER_ID, _
from odoo.modules.registry import RegistryManager
from odoo.http import Root
import werkzeug
import base64
import time
import json
import logging

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

def authenticate(token):
    try:
        a = 4 - len(token) % 4
        if a != 0:
            token += '==' if a == 2 else '='
        SERVER,db,login,uid,ts = base64.urlsafe_b64decode(str(token)).split(',')
        if int(ts) + 60*60*24*7*10 < time.time():
            return False
        registry = RegistryManager.get(db)
        cr = registry.cursor()
        env = api.Environment(cr, int(uid), {})
    except Exception,e:
        return str(e)
    return env

class NxtRestfulApi(http.Controller):
    @http.route([
        '/api/v1.0/get_token',
        ], type='http', auth="none", csrf=False, methods=['POST','GET'])
    def get_token(self,serv='http://d10.appnxt.com', a=None, s='admin', d='d10', sid=None, success=True, message='',**kw):
        """ service, app(user/login),secret(password) """
        try:
            uid = http.request.session.authenticate(d, a, s)
        except Exception,e:
            rp = {'token': '','success':False,'message':str(e)}
            return json_response(rp)
        if not uid:
            rp = {'token': '','success':False,'message':'you are unauthenticated'}
            return json_response(rp)
        e = base64.urlsafe_b64encode(','.join([serv,d,a,str(uid),str(int(time.time()))]))
        rp = {'token': e.replace('=',''),'success':success,'message':message}
        return json_response(rp)

    @http.route([
        '/api/v1.0/<string:model>',
        '/api/v1.0/<string:model>/<string:ids>'
        ], auth='none', type='http', csrf=False, methods=['GET'])
    def read_objects(self, model=None, ids=None, **kw):
        success, message,result,count,offset,limit = True,'','',0,0,80
        token = kw.pop('token')
        env = authenticate(token)
        if not env:
            return no_token()
        domain = eval(kw.get('filter',"[]"))
        fields = eval(kw.get('fields',"[]"))
        offset = int(kw.get('page','1')) - 1
        limit = int(kw.get('per_page','80'))
        order = kw.get('order','id')

        if ids:
            ids = map(int,ids.split(','))
            domain += [('id','in',ids)]
        try:
            count = env[model].search_count(domain)
            result = env[model].search_read(domain,fields,offset*limit,limit,order)
            model_fields = env[model].fields_get()
            for r in result:
                for f in r.keys():
                    if model_fields[f]['type'] == 'many2one':
                        if r[f]:
                            r[f] = {'id': r[f][0],'display_name':r[f][1]}
                        else:
                            r[f] = ''
            if ids and result and len(ids) == 1:
                result = result[0]
        except Exception,e:
            result,success,message = '',False,str(e)
        rp = {'success': success,'message':message, 'result': result,'total':count,'page': offset+1, 'per_page': limit}
        return json_response(rp)

    @http.route([
        '/api/v1.0/<string:model>',
        ], auth='none', type='http', csrf=False, methods=['POST'])
    def create_objects(self, model=None, success=True, message='', **kw):
        token = kw.pop('token')
        env = authenticate(token)
        if not env:
            return no_token()
        try:
            result = env[model].create(kw).id
        except Exception,e:
            result,success,message = '',False,str(e)
        env.cr.commit()
        env.cr.close()
        rp = {'result': result,'success': success,'message':message}
        return json_response(rp)

    @http.route([
        '/api/v1.0/<string:model>/<string:ids>',
        ], auth='none', type='http', csrf=False, methods=['PUT','PATCH'])
    def update_objects(self, model=None, ids=None, success=True, message='', **kw):
        token = kw.pop('token')
        env = authenticate(token)
        if not env:
            return no_token()
        ids = map(int,ids.split(','))
        try:
            result = env[model].browse(ids).write(kw)
        except Exception, e:
            result,success,message = '',False,str(e)
        env.cr.commit()
        env.cr.close()
        rp = {'result': result,'success': success,'message':message}
        return json_response(rp)

    @http.route([
        '/api/v1.0/<string:model>/<string:ids>',
        ], auth='none', type='http', csrf=False, methods=['DELETE'])
    def unlink_objects(self, model=None, ids=None, success=True, message='', **kw):
        token = kw.pop('token')
        env = authenticate(token)
        if not env:
            return no_token()
        ids = map(int,ids.split(','))
        try:
            result = env[model].browse(ids).unlink()
        except Exception, e:
            result,success,message = '',False,str(e)
        env.cr.commit()
        env.cr.close()
        rp = {'result': result,}
        return json_response(rp)

    @http.route([
        '/api/v1.0/<string:model>/call/<string:method>',
        ], auth='none', type='http', csrf=False, methods=['POST','GET'])
    def call_method(self, model=None, method=None, success=True, message='', **kw):
        token = kw.pop('token')
        env = authenticate(token)
        if not env:
            return no_token()
        try:
            result = eval('env[model].'+method)(kw)
        except Exception, e:
            result,success,message = '',False,str(e)
        env.cr.commit()
        env.cr.close()
        response = {'result': result,'success': success,'message':message}
        if isinstance(result,dict) and result.get('pagination'):
            response.update(result.pop('pagination'))
            response.update({'result': result.pop('results')})
        return json_response(response)
