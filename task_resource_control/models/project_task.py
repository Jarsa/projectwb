# -*- coding: utf-8 -*-
# <2015> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"
    _name = "project.task"

    resource_control_ids = fields.One2many(
        'resource.control',
        'task_id',
        string='Resource change history')
    real_qty = fields.Float(
        string='Real Quantity',
        readonly=True, )
    real_subtotal = fields.Float(
        string='Real Subtotal',
        compute='_compute_real_subtotal',)
    qty = fields.Float(string='Planned Quantity',)

    @api.depends('real_qty')
    @api.multi
    def _compute_real_subtotal(self):
        for rec in self:
            rec.real_subtotal = rec.unit_price * rec.real_qty

    @api.multi
    def _update_real_qty(self):
        for rec in self:
            for resource in rec.resource_line_ids:
                resource.real_qty = rec.real_qty * resource.qty
