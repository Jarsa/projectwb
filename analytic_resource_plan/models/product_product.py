# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductProduct(models.Model):

    _name = 'product.product'
    _description = 'product product'

    state = fields.Selection(
        [('hr', 'Human Resources'),
         ('product', 'Product'),
         ('concept', 'Concept')],
        required=True, string='Status')
