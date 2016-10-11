# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ToolsResources(models.Model):
    _name = 'tools.resources'
    _description = 'Tools Resources Model'

    product_id = fields.Many2one(
        'product.product',
        domain=[('categ_id', '=', 'Herramientas')],
        required=True,
        string='Resource')
    product_qty = fields.Float(
        required=True,
        default=1.0,
        string='Quantity',
        )
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Unit of Measure',
        required=True,
        )
    analytic_resource_plan_line_id = fields.Many2one(
        'analytic.resource.plan.line',
        string='Resource plan id')
    unit_price = fields.Float(required=True)
    subtotal = fields.Float(required=True)
