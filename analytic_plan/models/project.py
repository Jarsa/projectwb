# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    version_id = fields.Many2one(
        'analytic.plan.version',
        string='Planning Version', required=True)
    expenses = fields.Float(default=50)
    utility = fields.Float(default=20)
