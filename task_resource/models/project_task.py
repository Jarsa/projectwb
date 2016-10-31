# -*- coding: utf-8 -*-
# 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"
    _name = "project.task"

    resource_ids = fields.One2many(
        comodel_name='task.resource',
        inverse_name='task_id',
        string='Task Resource',
        copy=True,
        store=True)
    resource_line_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='task_resource_id',
        store=True
        )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )
    subtotal = fields.Float()
    unit_price = fields.Float()

    @api.multi
    @api.depends('qty', 'unit_price')
    def _compute_value_subtotal(self):
        for rec2 in self:
            rec2.subtotal = rec2.qty * rec2.unit_price
