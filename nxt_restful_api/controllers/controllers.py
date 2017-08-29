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
import _ast
import re
import csv
try:                    # Python 3
    import configparser
    from threading import current_thread
    from xmlrpc.client import Fault, ServerProxy, MININT, MAXINT
    PY2 = False
except ImportError:     # Python 2
    import ConfigParser as configparser
    from threading import currentThread as current_thread
    from xmlrpclib import Fault, ServerProxy, MININT, MAXINT
    PY2 = True

DOMAIN_OPERATORS = frozenset('!|&')
_term_re = re.compile(
    '([\w._]+)\s*'  '(=(?:like|ilike|\?)|[<>]=?|!?=(?!=)'
    '|(?<= )(?:like|ilike|in|not like|not ilike|not in|child_of))'  '\s*(.*)')
# Simplified ast.literal_eval which does not parse operators
def _convert(node, _consts={'None': None, 'True': True, 'False': False}):
    if isinstance(node, _ast.Str):
        return node.s
    if isinstance(node, _ast.Num):
        return node.n
    if isinstance(node, _ast.Tuple):
        return tuple(map(_convert, node.elts))
    if isinstance(node, _ast.List):
        return list(map(_convert, node.elts))
    if isinstance(node, _ast.Dict):
        return dict([(_convert(k), _convert(v))
                     for (k, v) in zip(node.keys, node.values)])
    if hasattr(node, 'value') and str(node.value) in _consts:
        return node.value         # Python 3.4+
    if isinstance(node, _ast.Name) and node.id in _consts:
        return _consts[node.id]   # Python <= 3.3
    raise ValueError('malformed or disallowed expression')

if PY2:
    int_types = int, long

    class _DictWriter(csv.DictWriter):
        """Unicode CSV Writer, which encodes output to UTF-8."""

        def writeheader(self):
            # Method 'writeheader' does not exist in Python 2.6
            header = dict(zip(self.fieldnames, self.fieldnames))
            self.writerow(header)

        def _dict_to_list(self, rowdict):
            rowlst = csv.DictWriter._dict_to_list(self, rowdict)
            return [cell.encode('utf-8') if hasattr(cell, 'encode') else cell
                    for cell in rowlst]
else:   # Python 3
    basestring = str
    int_types = int
    _DictWriter = csv.DictWriter

def literal_eval(expression, _octal_digits=frozenset('01234567')):
    node = compile(expression, '<unknown>', 'eval', _ast.PyCF_ONLY_AST)
    if expression[:1] == '0' and expression[1:2] in _octal_digits:
        raise SyntaxError('unsupported octal notation')
    value = _convert(node.body)
    if isinstance(value, int_types) and not MININT <= value <= MAXINT:
         raise ValueError('overflow, int exceeds XML-RPC limits')
    return value

def searchargs(params, kwargs=None, context=None):
    """Compute the 'search' parameters."""

    if not params:
        return ([],)
    domain = params[0]
    if not isinstance(domain, list):
        return params
    for (idx, term) in enumerate(domain):
        if isinstance(term, basestring) and term not in DOMAIN_OPERATORS:
            m = _term_re.match(term.strip())
            if not m:
                raise ValueError('Cannot parse term %r' % term)
            (field, operator, value) = m.groups()
            try:
                value = literal_eval(value)
            except Exception:
                # Interpret the value as a string
                pass
            domain[idx] = (field, operator, value)
    return domain

def issearchdomain(arg):
    """Check if the argument is a search domain.

    Examples:
      - ``[('name', '=', 'mushroom'), ('state', '!=', 'draft')]``
      - ``['name = mushroom', 'state != draft']``
      - ``[]``
    """
    return isinstance(arg, list) and not (arg and (
        # Not a list of ids: [1, 2, 3]
        isinstance(arg[0], int_types) or
        # Not a list of ids as str: ['1', '2', '3']
        (isinstance(arg[0], basestring) and arg[0].isdigit())))

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

        domain = searchargs(domain)

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
