
# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class TotalTaskResource(models.Model):
    _name = "total.task.resource"

    uom_id = fields.Many2one(
        'product.uom',
        string='UoM',
        required=True
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )
    subtotal = fields.Float(
        # compute='compute_value_subtotal')
    )
    unit_price = fields.Float(required=True)
    qty_total = fields.Float(required=True)
