# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class StockPickingType(models.Model):
    _name = 'stock.picking.type'
    _inherit = 'stock.picking.type'

    active = fields.Boolean(default=True,)
