# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectWbsElement(models.Model):
    _description = "Project WBS Element"
    _inherit = 'project.wbs_element'

    analytic_billing_id = fields.Many2one('analytic.billing.plan')
    button_billing = fields.Boolean(compute="_compute_button_billing")
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    product_id = fields.Many2one('product.product', string='Product')
    unit_price = fields.Float(
        string="Unit Price",
        readonly=True,
        compute='_compute_unit_price')
    quantity = fields.Float()
    total = fields.Float(compute="_compute_total")
    quantity_invoice = fields.Float()
    remaining_quantity = fields.Float()

    @api.depends('unit_price', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.unit_price

    @api.depends('product_id')
    def _compute_unit_price(self):
        for rec in self:
            if rec.product_id:
                rec.product_uom_id = rec.product_id.uom_id
                rec.unit_price = rec.product_id.lst_price

    @api.depends('parent_id')
    def _compute_button_billing(self):
        for wbs_element in self:
            if (wbs_element.parent_id and not wbs_element.parent_id.parent_id):
                wbs_element.button_billing = True
            else:
                wbs_element.button_billing = False
