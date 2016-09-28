# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AnalyticResourcePlanLine(models.Model):
    _name = 'analytic.resource.plan.line'
    _description = "Analytic Resource Planning lines"

    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account', required=True,
        )
    name = fields.Char(
        string='Activity description', required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Datetime(
        required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=fields.Datetime.now())
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        required=True, readonly=True,
        help=' * The \'Draft\' status is used when a user is encoding '
             'a new and unconfirmed resource plan line. '
             '\n* The \'Confirmed\' status is used for to confirm the '
             'execution of the resource plan lines.',
        default='draft')
    product_id = fields.Many2one(
        'product.product', string='Product',
        readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    product_uom_id = fields.Many2one(
        'product.uom', string='UoM', required=True,
        readonly=True, states={'draft': [('readonly', False)]})
    unit_amount = fields.Float(
        string='Planned Quantity', readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        help='Specifies the quantity that has been planned.',
        default=1)
    notes = fields.Text()
    parent_id = fields.Many2one(
        'analytic.resource.plan.line',
        string='Parent', readonly=True,)
    child_ids = fields.One2many(
        'analytic.resource.plan.line',
        'parent_id', string='Child lines')
    has_child = fields.Boolean(string="Child lines")
    analytic_line_plan_ids = fields.One2many(
        'analytic.plan', 'resource_plan_id',
        string='Planned costs', readonly=True)

    @api.onchange('account_id')
    def _onchange_account_id(self):
         if self.account_id:
            self.date = self.account_id.create_date
