# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    income_ids = fields.One2many(
        'project.income', 'project_id', string='Income')
    total_income = fields.Float(compute='_compute_total_income')
    total_expense = fields.Float(compute='_compute_total_expenses')
    balance = fields.Float(compute='_compute_balance')

    @api.multi
    def _compute_total_income(self):
        for rec in self:
            rec.total_income = sum(rec.income_ids.mapped('amount_total'))

    @api.multi
    def _compute_total_expenses(self):
        for rec in self:
            rec.total_expense = sum(rec.task_ids.mapped('subtotal'))

    @api.multi
    def _compute_balance(self):
        for rec in self:
            rec.balance = rec.total_income - rec.total_expense
