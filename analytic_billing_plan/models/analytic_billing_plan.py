# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class AnalyticBillingPlan(models.Model):
    _name = 'analytic.billing.plan'
    _description = "Analytic Billing Plan"
    _inherit = 'analytic.plan'

    customer_id = fields.Many2one(
        'res.partner', string="Customer", readonly=True)
    has_active_order = fields.Boolean(
        string='Billing request',
        help="Indicates that this billing plan line "
        "contains at least one non-cancelled billing request.")
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        required=True, readonly=True,
        default='draft')
    quantity = fields.Float()
    concept = fields.Many2one('product.product')
    price_unit = fields.Float("Price Unit")

    @api.onchange('account_id')
    def _onchange_account(self):
        if self.account_id:
            self.customer_id = self.account_id.partner_id

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id
            self.price_unit = self.product_id.lst_price

    @api.onchange('unit_amount', 'price_unit')
    def _compute_amount(self):
        for rec in self:
            rec.amount_currency = rec.price_unit * rec.unit_amount
