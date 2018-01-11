# -*- coding: utf-8 -*-
from odoo import http

# class AutoResetSequence(http.Controller):
#     @http.route('/auto_reset_sequence/auto_reset_sequence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/auto_reset_sequence/auto_reset_sequence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('auto_reset_sequence.listing', {
#             'root': '/auto_reset_sequence/auto_reset_sequence',
#             'objects': http.request.env['auto_reset_sequence.auto_reset_sequence'].search([]),
#         })

#     @http.route('/auto_reset_sequence/auto_reset_sequence/objects/<model("auto_reset_sequence.auto_reset_sequence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('auto_reset_sequence.object', {
#             'object': obj
#         })