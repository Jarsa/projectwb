# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProjectWbsElement(models.Model):
    _name = "project.wbs_element"
    _description = "Project WBS Element"
    _inherit = "project.wbs_element"

    button_resource = fields.Boolean(
        default=False, compute="_compute_button_resource")
    nbr_resource = fields.Integer(
        string="Resource Plan",
        compute='_count_resource')
    resource_ids = fields.One2many(
        'resources',
        'wbs_element_id',
        compute='_compute_wbs_resource'
    )

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

    @api.depends('resource_ids')
    def _compute_wbs_resource(self):
        for rec in self:
            rec.resource_ids.unlink()
            resources = self.env['analytic.resource.plan.line'].search(
                [('account_id', '=', rec.analytic_account_id.id)])

            for resource in resources:
                rec.resource_ids.create({
                    'name': resource.name,
                    'product_qty': resource.product_qty,
                    'product_uom_id': resource.product_uom_id,
                    'unit_price': resource.unit_price,
                    'subtotal': resource.subtotal,
                    'resource_type': resource.resource_type,
                    'qty_on_hand': resource.qty_on_hand,
                    'consume': resource.consume,
                    'location': resource.location,
                    'wbs_element_id': rec.id
                    })
