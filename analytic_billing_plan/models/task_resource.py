# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class TaskResource(models.Model):
    _description = "Task Resource"
    _inherit = 'project.task'

    line_billing_ids = fields.One2many('analytic.billing.plan', 'billing_id')
    nbr_billing = fields.Float(
        string="Billing Request",
        compute="_compute_nrb_billing")
    remaining_quantity = fields.Float(default=0.0)
    quantity_invoice = fields.Float()
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    tax_ids = fields.Many2many('account.tax', string="Taxes")

    @api.depends('line_billing_ids')
    def _compute_nrb_billing(self):
        for record in self:
            record.nbr_billing = len(record.line_billing_ids.search(
                [('product_id', '=', record.id)]))

    @api.multi
    def request_billing_request(self):
        return {
            'name': 'Billing Request',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.billing.plan',
            'domain': [('account_id', '=', self.analytic_account_id.id)],
            'type': 'ir.actions.act_window',
        }
