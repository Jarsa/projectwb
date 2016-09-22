# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models



class AnalyticPlan(models.Model):
    _name = 'analytic.plan'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Analytic Plan'

    name = fields.Char(string='Activity description', required=True)
    date = fields.Date('Date', required=True)
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
    currency_id = fields.Many2one('res.currency', string='Currency')
    account_id = fields.Many2one(
        string='Analytic Account', required=True)
    user_id = fields.Many2one('res.users', 'User')
    company_id = fields.Many2one(
        'res.company', string='Company',
        readonly=True)
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    product_id = fields.Many2one('product.product', string='Product')
    general_account_id = fields.Many2one(
        'account.account', string='General Account',
        required=True)
    journal_id = fields.Many2one(
        string='Planning Analytic Journal', required=True)
    code = fields.Char()
    ref = fields.Char()
    notes = fields.Text()
    version_id = fields.Many2one(
        string='Planning Version', required=True)
