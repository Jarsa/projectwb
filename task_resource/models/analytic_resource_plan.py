# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
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
    date = fields.Date(required=True, default=fields.Date.today)
    qty = fields.Float(required=True, string="Quantity")
    subtotal = fields.Float(required=True, compute='compute_value_subtotal')
    unit_price = fields.Float(required=True)

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

    @api.multi
    @api.depends('qty', 'unit_price')
    def compute_value_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.unit_price
