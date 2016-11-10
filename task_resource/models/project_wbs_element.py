# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProjectWbsElement(models.Model):
    _name = "project.wbs_element"
    _inherit = "project.wbs_element"

    total_concept_expense = fields.Float(
        string='Billing Total',
        compute='_compute_total_concept_expense')

    @api.multi
    def _compute_total_concept_expense(self):
        for rec in self:
            tasks = self.env['project.task'].search([
                ('wbs_element_id', '=', rec.id)])
            if tasks:
                for task in tasks:
                    rec.total_concept_expense += task.total_expense
            else:
                rec.total_concept_expense = 0.0
