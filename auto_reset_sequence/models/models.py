# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.iap.models.iap import jsonrpc, InsufficientCreditError


DEFAULT_ENDPOINT = 'http://iap-service.y11c.appnxt.com'
class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    auto_reset = fields.Boolean('Auto Reset',default=False)
    reset_period = fields.Selection(
            [('year', 'Every Year'), ('month', 'Every Month'), ('woy', 'Every Week'), ('day', 'Every Day'), ('h24', 'Every Hour'), ('min', 'Every Minute'), ('sec', 'Every Second')],
            'Reset Period', required=True, default='day')
    reset_time = fields.Char('Reset Time', size=64, help="")
    reset_init_number = fields.Integer('Reset Number', required=True, default=1, help="Reset number of this sequence")

    @api.model
    def create(self, vals):
        res = super(IrSequence,self).create(vals)
        self.filtered(lambda x: x.auto_reset == True).endpoint_set_sequence()
        return res

    @api.multi
    def write(self, vals):
        res = super(IrSequence,self).write(vals)
        self.filtered(lambda x: x.auto_reset == True).endpoint_set_sequence()
        return res

    @api.model
    def next_by_code(self, sequence_code):
        seq = self.search([('code','=',sequence_code)],limit=1)
        if seq and seq.auto_reset:
            return self.action_get_sequence(sequence_code)
        return super(IrSequence,self).next_by_code(sequence_code)

    @api.multi
    def endpoint_set_sequence(self):
        for r in self:
            user_token = self.env['iap.account'].get('auto_reset_sequence')
            params = {
                'dbuuid': self.env['ir.config_parameter'].sudo().get_param('database.uuid'),
                'account_token': user_token.account_token,
                'code': r.code,
                'vals': r.read()[0]
            }
            endpoint = self.env['ir.config_parameter'].sudo().get_param('auto_reset_sequence.endpoint', DEFAULT_ENDPOINT)
            jsonrpc(endpoint + '/set_sequence', params=params)
        return True

    @api.multi
    def action_get_sequence(self,sequence_code):
        user_token = self.env['iap.account'].get('auto_reset_sequence')
        params = {
            'account_token': user_token.account_token,
            'dbuuid': self.env['ir.config_parameter'].sudo().get_param('database.uuid'),
            'code': sequence_code,
        }
        endpoint = self.env['ir.config_parameter'].sudo().get_param('auto_reset_sequence.endpoint', DEFAULT_ENDPOINT)
        return jsonrpc(endpoint + '/sequence', params=params)