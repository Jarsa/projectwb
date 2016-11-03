# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class AnalyticPlan(models.Model):
    _name = 'analytic.plan'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Analytic Plan'

    name = fields.Char(string='Activity description', required=True)
    date = fields.Date('Date', required=True, default=fields.Date.today)
    amount = fields.Float(
        string='Amount', required=True,
        help=('Calculated by multiplying the quantity '
              'and the price given in the Product\'s '
              'cost price. Always expressed in the '
              'company main currency.'))
    amount_currency = fields.Float(
        string='Amount Currency',
        help="The amount expressed in an optional other currency.")
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        readonly=True)
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    product_id = fields.Many2one('project.task', string='Product')
    general_account_id = fields.Many2one(
        'account.account', string='General Account',
        required=True)
    journal_id = fields.Many2one(
        'analytic.plan.journal',
        string='Planning Analytic Journal')
    code = fields.Char()
    ref = fields.Char()
    notes = fields.Text()
    version_id = fields.Many2one(
        'analytic.plan.version',
        string='Planning Version')
    project_id = fields.Many2one(
        'project.project',
        string='Project')
    analytic_plan_version = fields.Many2one(
        'analytic.plan.version',
        string='Version')

    @api.multi
    @api.constrains('amount_currency', 'amount')
    def _check_amount(self):
        for rec in self:
            expense = (rec.journal_id.type in ['purchase', 'general'])
            income = (rec.journal_id.type in ['sale', 'cash'])
            if expense and rec.amount_currency > 0.0:
                raise exceptions.ValidationError(
                    _('The amount must be negative because the type'
                        ' of journal represents an expense.'))
            elif income and rec.amount_currency < 0.0:
                raise exceptions.ValidationError(
                    _('The amount must be positive because the type'
                        ' of journal represents an income.'))

    @api.onchange('currency_id', 'amount_currency')
    def _onchange_currency_id(self):
        for rec in self:
            if rec.currency_id.id:
                total = rec.currency_id.compute(
                    rec.amount_currency,
                    self.env.user.company_id.currency_id)
                rec.amount = total
