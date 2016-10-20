
# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.exceptions import ValidationError, Warning
from openerp.tools.translate import _


class TotalTaskResource(models.Model):
    _name = "total.task.resource"

    resource_line_ids = fields.One2many(
        'analytic.resource.plan.line',
        'task_resource_id')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
        required=True
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )
    subtotal = fields.Float(compute='compute_value_subtotal')
    unit_price = fields.Float(required=True)
    qty_total = fields.Float(required=True)

    @api.multi
    @api.depends('qty', 'unit_price')
    def compute_value_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.unit_price
