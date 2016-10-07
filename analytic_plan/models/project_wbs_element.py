# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectWbsElement(models.Model):
    _name = "project.wbs_element"
    _description = "Project WBS Element"
    _inherit = 'project.wbs_element'

    analytic_plan_version_id = fields.Many2one(
        'analytic.plan.version',
        string='Current Plan Version',
        readonly=True, compute='_compute_version')

    @api.depends('project_id')
    def _compute_version(self):
        for rec in self:
            if rec.project_id:
                rec.analytic_plan_version_id = rec.project_id.version_id
