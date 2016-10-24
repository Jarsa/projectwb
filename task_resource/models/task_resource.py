# -*- coding: utf-8 -*-
# 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class TaskResource(models.Model):
    _name = "task.resource"
    _description = "Task Resource"

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
    )
    description = fields.Char('Description', required=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='product',
    )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        description = ''
        uom_id = False
        product = self.product_id
        if product:
            description = product.name_get()[0][1]
            uom_id = product.uom_id.id
        if product.description_sale:
            description += '\n' + product.description_sale
        self.description = description
        self.uom_id = uom_id
