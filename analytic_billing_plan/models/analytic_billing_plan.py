# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class AnalyticBillingPlan(models.Model):
    _name = 'analytic.billing.plan'
    _description = "Analytic Billing Plan"

    customer_id = fields.Many2one(
        'res.partner', string="Customer", readonly=True)
    has_active_order = fields.Boolean(
        string='Billing request',
        help="Indicates that this billing plan line "
        "contains at least one non-cancelled billing request.",
        default=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        required=True, readonly=True,
        default='draft')
    quantity = fields.Float()
    price_unit = fields.Float("Price Unit")
    invoice_id = fields.Many2one('account.invoice')
    name = fields.Char(string='Activity description', required=True)
    date = fields.Date('Date', required=True, default=fields.Date.today)
    amount = fields.Float(
        string='Amount', required=True,
        help=('Calculated by multiplying the quantity '
              'and the price given in the Product\'s '
              'cost price. Always expressed in the '
              'company main currency.'))
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    account_id = fields.Many2one('account.account', 'Account')
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        readonly=True)
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    task_id = fields.Many2one('project.task', string='Concept')
    general_account_id = fields.Many2one(
        'account.account', string='General Account',)
    ref = fields.Char()
    project_id = fields.Many2one(
        'project.project',
        string='Project')

    @api.multi
    def action_button_confirm(self):
        for rec in self:
            rec.write({'state': 'confirm'})

    @api.multi
    def action_button_draft(self):
        for rec in self:
            rec.invoice_id.unlink()
            rec.write({'state': 'draft'})

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.invoice_id:
                raise ValidationError(
                    _('You can not delete a billing request'
                      'with invoice'))
            else:
                return super(AnalyticBillingPlan, self).unlink()
