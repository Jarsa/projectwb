# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AnalyticResourcePlanLine(models.Model):
    _name = "analytic.resource.plan.line"
    _description = "Resource Plan"

    task_resource_id = fields.Many2one(
        'project.task',
    )
    product_id = fields.Many2one(
        'product.product',
        string="Product")
    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account')
    date = fields.Date(default=fields.Date.today)
    qty = fields.Float(string="Quantity")
    subtotal = fields.Float()
    unit_price = fields.Float()
    description = fields.Char('Description')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    purchase_request_ids = fields.Many2many(
        comodel_name='purchase.request',
        string='Purchase Requests')
    resource_type_id = fields.Many2one(
        'resource.type',
        string='Resources types')

    real_qty = fields.Float(string="Quantity Real")
    requested_qty = fields.Float(string="Requestes Quantity")

    @api.onchange('product_id')
    def onchange_product(self):
        self.description = self.product_id.description
        self.uom_id = self.product_id.uom_id
        self.account_id = self.task_resource_id.analytic_account_id
