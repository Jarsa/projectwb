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
    qty = fields.Float(string="Quantity", default="1")
    subtotal = fields.Float()
    unit_price = fields.Float()
    description = fields.Char('Description')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )

    @api.onchange('product_id')
    def onchange_product(self):
        self.description = self.product_id.description
        self.uom_id = self.product_id.uom_id

    @api.model
    def default_get(self, field):
        if 'active_id' in self.env.context:
            record_id = self.env.context['active_id']
            plan = self.env['project.wbs_element'].search(
                [('id', '=', record_id)])
            res = super(AnalyticResourcePlanLine, self).default_get(field)
            res.update({'account_id': plan.analytic_account_id.id})
            res.update(domain={
                'account_id': plan.analytic_account_id.id
            })
            return res
        else:
            return super(AnalyticResourcePlanLine, self).default_get(field)
