# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AnalyticPlan(models.Model):
    _inherit = 'analytic.plan'

    resource_plan_id = fields.Many2one(
        'analytic.resource.plan.line', string='Resource Plan Line')
