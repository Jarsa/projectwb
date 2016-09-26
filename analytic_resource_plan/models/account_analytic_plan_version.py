# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AnalyticPlanVersion(models.Model):
    _inherit = 'analytic.plan.version'

    default_resource_plan = fields.Boolean(
        string='Default for resource plan')
