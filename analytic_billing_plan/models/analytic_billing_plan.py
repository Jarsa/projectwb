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
    invoice_id = fields.Many2one('account.invoice')

    @api.onchange('account_id')
    def _onchange_account(self):
        if self.account_id:
            self.customer_id = self.account_id.partner_id

    @api.multi
    def action_button_confirm(self):
        for rec in self:
            invoice = {
                'partner_id': rec.customer_id.id,
                'reference': rec.ref,
                'fiscal_position_id': (
                    rec.customer_id.property_account_position_id.id),
                'currency_id': rec.currency_id.id,
                'account_id': (
                    rec.customer_id.property_account_receivable_id.id),
                'type': 'out_invoice',
                'invoice_line_ids': [(0, False, {
                    'product_id': rec.product_id.id,
                    'quantity': rec.unit_amount,
                    'price_unit': rec.price_unit,
                    'invoice_line_tax_ids': [
                        (6, 0, [x.id for x in rec.product_id.tax_ids])],
                    'name': rec.product_id.name,
                    'account_id': rec.product_id.account_id.id})]
            }

            invoice_id = self.env['account.invoice'].create(invoice)
            rec.write({'invoice_id': invoice_id.id})
