# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from openerp import api, fields, models


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    product_qty = fields.Float(
        digits=(14, 5),
        string='Quantity',)
    qty_on_hand = fields.Float(
        string="Quantity on Hand",
        digits=(14, 5),
        compute="_compute_qty_on_hand",
    )
    is_project_insume = fields.Boolean(
        string='Is Project Insume?',)

    @api.multi
    def _compute_qty_on_hand(self):
        for rec in self:
            products = self.env['stock.quant'].search(
                [('product_id', '=', rec.product_id.id),
                 ('location_id', '=',
                    rec.request_id.project_id.location_id.id)])
            if products:
                for product in products:
                    rec.qty_on_hand += product.qty
            else:
                rec.qty_on_hand = 0
