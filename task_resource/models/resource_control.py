# -*- coding: utf-8 -*-
# <2015> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class ResourceControl(models.Model):
    _name = "resource.control"
    _description = "Control the quantity of insumes used in a task"

    insume_explotion_id = fields.Many2one(
    	'analytic.resource.plan.line',
    	string="Insume explotion")
    task_id = fields.Many2one('project.task', string="Task")
    type = fields.Selection([
    	('deductively', "Deductively"),
    	('additive', "Additive")])
    reason = fields.Html()
    state = fields.Selection([
        ('pending', "Pending"),
        ('approved', "Approve"),
        ('reject', "Reject"),
    ], default='pending')

    @api.multi
    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    @api.multi
    def action_reject(self):
        for rec in self:
            rec.state = 'reject'

    @api.multi
    def action_pending(self):
        for rec in self:
            rec.state = 'pending'
