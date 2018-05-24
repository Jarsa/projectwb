# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    product_id = fields.Many2one(
        'product.product',
        string='Product to Billing',
        domain=[('sale_ok', '=', True),
                ('type', '=', 'service')],
        )
