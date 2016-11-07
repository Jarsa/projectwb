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
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic account')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        required=True, readonly=True,
        default='draft')
    resource_line_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='task_resource_id',
        store=True,
        compute='_compute_resources_line_ids'
        )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )
    subtotal = fields.Float(compute='_compute_value_subtotal')
    unit_price = fields.Float()

    @api.multi
    @api.depends('qty', 'unit_price')
    def _compute_value_subtotal(self):
        for rec2 in self:
            rec2.subtotal = rec2.qty * rec2.unit_price

    @api.multi
    def write(self, values):
        for rec in self:
            res = super(ProjectTask, self).write(values)
            resources = self.env['analytic.resource.plan.line'].search([
                ('task_resource_id', '=', rec.id)])
            if not resources:
                for resource in rec.resource_ids:
                    rec.resource_line_ids.create({
                        'task_resource_id': rec.id,
                        'account_id': resource.account_id.id,
                        'product_id': resource.product_id.id,
                        'description': resource.description,
                        'resource_type': resource.resource_type,
                        'uom_id': resource.uom_id.id,
                        'qty': rec.qty * resource.qty,
                        'real_qty': rec.qty * resource.qty,
                        'subtotal': (
                            rec.qty * resource.qty * (
                                resource.product_id.lst_price))
                    })
            else:
                for item in resources:
                    if not item.purchase_request_ids and rec.state == 'draft':
                        item.unlink()
                for resource in rec.resource_ids:
                    for line in resources:
                        if resource.product_id != line.product_id:
                            rec.resource_line_ids.create({
                                'task_resource_id': rec.id,
                                'account_id': resource.account_id.id,
                                'product_id': resource.product_id.id,
                                'description': resource.description,
                                'resource_type': resource.resource_type,
                                'uom_id': resource.uom_id.id,
                                'qty': rec.qty * resource.qty,
                                'real_qty': rec.qty * resource.qty,
                                'subtotal': (
                                    rec.qty * resource.qty * (
                                        resource.product_id.lst_price))
                            })
        return res

    @api.multi
    @api.depends('resource_line_ids')
    def _compute_resources_line_ids(self):
        for rec in self:
            resources = rec.resource_line_ids.search(
                [('task_resource_id', '=', rec.id)])
            for resource in resources:
                rec.update({'resource_line_ids': resource})

    @api.multi
    def insume_explotion(self):
        return {
            'name': 'Insume Explotion',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.resource.plan.line',
            'domain': [('account_id', '=', self.analytic_account_id.id)],
            'type': 'ir.actions.act_window'}

    @api.multi
    def action_button_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    @api.multi
    def action_button_draft(self):
        for rec in self:
            rec.state = 'draft'
