# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AnalyticResourcePlanLine(models.Model):
    _name = 'analytic.resource.plan.line'
    _description = "Analytic Resource Planning lines"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account', required=True)
    name = fields.Char(
        string='Sequence', readonly=True)
    date = fields.Date(required=True, default=fields.Date.today)

    
