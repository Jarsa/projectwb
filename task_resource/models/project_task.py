
# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
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
        compute='compute_resource_concepts',
        )
    concept_line_ids = fields.One2many(
        comodel_name='concepts',
        inverse_name='concept_resource_id',)
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

    @api.multi
    @api.depends('qty', 'unit_price')
    def compute_value_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.unit_price

    @api.multi
    @api.depends('resource_ids', 'qty')
    def compute_resource_concepts(self):
        for rec in self:
            for item in rec.resource_line_ids:
                item.unlink()
            if rec.resource_ids:
                for record in rec.resource_ids:
                    rec.resource_line_ids += rec.resource_line_ids.create({
                        'product_id': record.product_id.id,
                        'account_id': rec.project_id.analytic_account_id.id,
                        'qty': record.qty * rec.qty,
                        'unit_price': record.product_id.lst_price,
                        'subtotal': rec.subtotal,
                        'task_resource_id': rec.id
                        })
