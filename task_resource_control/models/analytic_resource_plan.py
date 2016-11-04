# -*- coding: utf-8 -*-
# <2015> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = "analytic.resource.plan.line"
    _name = "analytic.resoruce.plan.line"

    wiz_id = fields.Many2one('resource.control.wizard')
