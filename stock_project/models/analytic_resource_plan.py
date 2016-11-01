# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AnalyticResourcePlanLine(models.Model):
    _name = "analytic.resource.plan.line"
    _description = "Resource Plan"
    _inherit = "analytic.resource.plan.line"

    qty = fields.Float(string="Quantity Planned")
    qty_on_hand = fields.Float(string="Quantity on Hand")
    qty_consumed = fields.Float(string="Quantity Consumed")
