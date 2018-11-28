# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectIncome(models.Model):
    _name = 'project.income'

    name = fields.Char(required=True)
    project_id = fields.Many2one(
        'project.project', required=True, readonly=True)
    income_type_id = fields.Many2one('project.income.type', required=True)
    qty = fields.Float()
    amount = fields.Float()
    amount_total = fields.Float(compute='_compute_amount_total', store=True)
    remaining_qty = fields.Float(compute='_compute_remaining_qty', store=True)
    amount_remaining = fields.Float(
        compute='_compute_amount_remaining', store=True)
    billing_ids = fields.One2many('analytic.billing.plan.line', 'income_id')

    @api.depends('qty', 'amount')
    @api.multi
    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = rec.qty * rec.amount

    @api.multi
    @api.depends('billing_ids', 'qty')
    def _compute_remaining_qty(self):
        for rec in self:
            rec.remaining_qty = rec.qty - sum(
                rec.billing_ids.mapped('quantity'))

    @api.multi
    @api.depends('remaining_qty', 'amount')
    def _compute_amount_remaining(self):
        for rec in self:
            rec.amount_remaining = rec.remaining_qty * rec.amount
