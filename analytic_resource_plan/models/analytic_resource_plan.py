# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


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
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        required=True, readonly=True,
        help=' * The \'Draft\' status is used when a user is encoding '
             'a new and unconfirmed resource plan line. '
             '\n* The \'Confirmed\' status is used for to confirm the '
             'execution of the resource plan lines.',
        default='draft')
    human_resources_ids = fields.Many2many(
        'human.resources',
        string='Human Resources')
    material_resources_ids = fields.One2many(
        'material.resources',
        'analytic_resource_plan_line_id',
        string='Material Resources')
    others_ids = fields.One2many(
        'others.resources',
        'analytic_resource_plan_line_id',
        string='Others')
    tools_ids = fields.One2many(
        'tools.resources',
        'analytic_resource_plan_line_id',
        string='Tools')
    equipment_ids = fields.Many2many(
        'equipment.resources',
        string='Equipment')
    indirects_ids = fields.Many2many(
        'indirects.resources',
        string='Indirect')
