# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id,
        required=True,)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product to Billing',
        domain=[('sale_ok', '=', True),
                ('type', '=', 'service')],
        compute="_get_product_id",
        inverse="_set_product_id",)

    @api.multi
    @api.depends('company_id')
    def _get_product_id(self):
        for rec in self:
            rec.product_id = rec.company_id.product_id.id

    @api.multi
    def _set_product_id(self):
        for rec in self:
            if rec.product_id != rec.company_id.product_id:
                rec.company_id.product_id = rec.product_id.id
