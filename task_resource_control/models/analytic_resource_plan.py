# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AnalyticResourcePlanLine(models.Model):
    _inherit = "analytic.resource.plan.line"

    real_qty = fields.Float(string="Quantity Real")
