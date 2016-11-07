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
    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account')
    description = fields.Char('Description')
    resource_type = fields.Selection(
        [('steel', 'Steel'),
         ('dust', 'Dust'),
         ('pyw', 'Paint & waterproofing'),
         ('fuel', 'Fuel'),
         ('ironmonger', 'Ironmonger'),
         ('wood', 'Wood'),
         ('hydro-sanitary', 'Hydro-Sanitary'),
         ('electric', 'Electric'),
         ('tool', 'Tool'),
         ('equipment', 'Equipment'),
         ('specialized-equipment', 'Specialized-Equipment'),
         ('workforce', 'Workforce'),
         ('stony', 'Stony'),
         ('concrete', 'Concrete'),
         ('services', 'Services'),
         ('aluminum&doors', 'Aluminum Works & Doors'),
         ('smithy', 'Smithy')], string='Resource Type',
        required=True, default='steel')

    @api.onchange('product_id')
    def onchange_product(self):
        self.account_id = self.task_id.analytic_account_id

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

    @api.model
    def default_get(self, field):
        if 'active_id' in self.env.context:
            record_id = self.env.context['active_id']
            plan = self.env['project.wbs_element'].search(
                [('id', '=', record_id)])
            res = super(TaskResource, self).default_get(field)
            res.update({'account_id': plan.analytic_account_id.id})
            res.update(domain={
                'account_id': plan.analytic_account_id.id
            })
            return res
        else:
            return super(TaskResource, self).default_get(field)
