# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    expense_analytic_plan_journal_id = fields.Many2one(
        'analytic.plan.journal',
        string='Cost Planning Analytic Journal')

