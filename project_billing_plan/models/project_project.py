# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    income_ids = fields.One2many(
        'project.income', 'project_id', string='Income')
    total_income = fields.Float(compute='_compute_total_income', store=True)
    total_expense = fields.Float(compute='_compute_total_expense', store=True)
    balance = fields.Float(compute='_compute_balance', store=True)
    total_income_real = fields.Float(readonly=True)
    total_expense_real = fields.Float(readonly=True)
    balance_real = fields.Float(readonly=True)

    @api.multi
    @api.depends('income_ids')
    def _compute_total_income(self):
        for rec in self:
            rec.total_income = sum(rec.income_ids.mapped('amount_total'))

    @api.multi
    @api.depends('task_ids')
    def _compute_total_expense(self):
        for rec in self:
            rec.total_expense = sum(rec.task_ids.mapped('subtotal'))

    @api.multi
    @api.depends('total_income', 'total_expense')
    def _compute_balance(self):
        for rec in self:
            rec.balance = rec.total_income - rec.total_expense

    @api.multi
    def compute_real_amounts(self):
        for rec in self:
            amls_income = self.env['account.move.line'].search([
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('account_id.user_type_id', 'in', [13, 14])])
            amls_expense = self.env['account.move.line'].search([
                ('analytic_account_id', '=', rec.analytic_account_id.id),
                ('account_id.user_type_id', 'in', [16, 17])])
            total_income_real = abs(sum(amls_income.mapped('balance')))
            total_expense_real = abs(sum(amls_expense.mapped('balance')))
            balance_real = total_income_real - total_expense_real
            rec.write({
                'total_expense_real': total_expense_real,
                'total_income_real': total_income_real,
                'balance_real': balance_real,
            })
