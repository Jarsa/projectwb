# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from openerp import fields, models


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    product_qty = fields.Float(
        digits=(14, 5),
        string='Quantity',)
    is_project_insume = fields.Boolean(
        string='Is Project Insume?',)
