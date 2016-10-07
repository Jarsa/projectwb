# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class ProjectWbsElement(models.Model):
    _description = "Project WBS Element"
    _inherit = 'project.wbs_element'

    billing_id = fields.Many2one(
        'billing.request', string='Billing', readonly=True)
    selec = fields.Boolean(default=False)
    analytic_billing = fields.Many2one('analytic.billing.plan')
