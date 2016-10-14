# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class Resources(models.Model):
    _name = 'resources'
    _description = 'Resources'

    name = fields.Char(
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
    unit_price = fields.Float(required=True)
    subtotal = fields.Float(required=True)
    resource_type = fields.Selection(
        [('human_resources', 'Human Resources'),
         ('materials', 'Materials'),
         ('others', 'Others'),
         ('tools', 'Tools'),
         ('equipment', 'Equipment'),
         ('indirect', 'Indirect')],
        string='Resources Type')
    resource_id = fields.Many2one('analytic.resource.plan.line')
    qty_on_hand = fields.Float(string="Quantity On Hand")
    consume = fields.Float(string="Consume")
    location = fields.Many2one('stock.location')
