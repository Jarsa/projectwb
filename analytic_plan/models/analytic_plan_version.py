# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AnalyticPlanVersion(models.Model):
    _name = 'analytic.plan.version'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Analytic Planning Version'

    name = fields.Char(string='Planning Version Name', required=True)
    code = fields.Char(string='Planning Version Code')
    active = fields.Boolean(
        help='If the active field is set to False, '
             'it will allow you to hide the analytic planning version '
             'without removing it.',
             default=True)
    notes = fields.Text()
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.user.company_id)
