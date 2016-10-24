# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
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
    unit_amount = fields.Float(
        string='Quantity',
        help='Specifies the amount of quantity to count.')
    amount_currency = fields.Float(
        string='Amount Currency',
        help="The amount expressed in an optional other currency.")
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account', required=True)
    user_id = fields.Many2one('res.users', 'User')
    company_id = fields.Many2one(
        'res.company', string='Company',
        readonly=True)
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    product_id = fields.Many2one('project.wbs.concept', string='Product')
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

    @api.onchange('unit_amount', 'product_id', 'journal_id')
    def _onchange_journal_id(self):
        for rec in self:
            if rec.journal_id.id and rec.product_id.id:
                expense = (rec.journal_id.type in ['purchase', 'general'])
                expense_account = (
                    rec.product_id.property_account_expense_id.id
                    if rec.product_id.property_account_expense_id.id
                    else
                    (rec.product_id.categ_id.
                        property_account_expense_categ_id.id)
                    if
                    (rec.product_id.categ_id.
                        property_account_expense_categ_id.id)
                    else False)
                income_account = (
                    rec.product_id.property_account_income_id.id
                    if rec.product_id.property_account_income_id.id
                    else
                    rec.product_id.categ_id.property_account_income_categ_id.id
                    if
                    rec.product_id.categ_id.property_account_income_categ_id.id
                    else False)
                if not expense_account or not income_account:
                    raise exceptions.ValidationError(
                        _('You must have assigned the expense / income'
                            ' accounts for the product. Please check it.'))
                if expense:
                    rec.general_account_id = expense_account
                    rec.amount_currency = (
                        (rec.product_id.list_price * rec.unit_amount) * -1)
                    rec.amount = (
                        rec.amount_currency if
                        rec.currency_id.id ==
                        self.env.user.company_id.currency_id.id
                        else rec._onchange_currency_id())
                else:
                    rec.general_account_id = income_account
                    rec.amount_currency = (
                        rec.product_id.list_price * rec.unit_amount)
                    rec.amount = (
                        rec.amount_currency if
                        rec.currency_id.id ==
                        self.env.user.company_id.currency_id.id
                        else rec._onchange_currency_id())
                rec.product_uom_id = rec.product_id.uom_id.id

    @api.onchange('currency_id', 'amount_currency')
    def _onchange_currency_id(self):
        for rec in self:
            if rec.currency_id.id:
                total = rec.currency_id.compute(
                    rec.amount_currency,
                    self.env.user.company_id.currency_id)
                rec.amount = total
