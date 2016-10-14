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
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        required=True, readonly=True,
        help=' * The \'Draft\' status is used when a user is encoding '
             'a new and unconfirmed resource plan line. '
             '\n* The \'Confirmed\' status is used for to confirm the '
             'execution of the resource plan lines.',
        default='draft')
    human_resources_ids = fields.One2many(
        'resources',
        'resource_id',
        string='Human Resources',
        domain=[('resource_type', '=', 'human_resources')])
    material_resources_ids = fields.One2many(
        'resources',
        'resource_id',
        string='Material Resources',
        domain=[('resource_type', '=', 'materials')])
    others_ids = fields.One2many(
        'resources',
        'resource_id',
        string='Others',
        domain=[('resource_type', '=', 'others')])
    tools_ids = fields.One2many(
        'resources',
        'resource_id',
        string='Tools',
        domain=[('resource_type', '=', 'tools')])
    equipment_ids = fields.One2many(
        'resources',
        'resource_id',
        string='Equipment',
        domain=[('resource_type', '=', 'equipment')])
    indirects_ids = fields.One2many(
        'resources',
        'resource_id',
        string='Indirect',
        domain=[('resource_type', '=', 'indirect')])

    @api.model
    def default_get(self, field):
        if 'active_id' in self.env.context:
            record_id = self.env.context['active_id']
            plan = self.env['project.wbs_element'].search(
                [('id', '=', record_id)])
            res = super(AnalyticResourcePlanLine, self).default_get(field)
            res.update({'account_id': plan.analytic_account_id.id})
            res.update(domain={
                'account_id': plan.analytic_account_id.id
            })
            return res
        else:
            return False
