# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductWbsElement(models.Model):
    _inherit = "project.wbs_element"

    button_resource = fields.Boolean(
        default=False, compute="_compute_button_resource")
    nbr_resource = fields.Integer(
        string="Resource Plan",
        compute='_count_resource')

    @api.depends('parent_id')
    def _compute_button_resource(self):
        for wbs_element in self:
            if (wbs_element.parent_id and not wbs_element.parent_id.parent_id):
                wbs_element.button_resource = True

    @api.depends('button_resource')
    def _count_resource(self):
        for record in self:
            record.nbr_resource = len(
                self.env['analytic.resource.plan.line'].search(
                    [('account_id', '=', record.analytic_account_id.id)]))
