# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _name = "purchase.request.line.make.purchase.order.item"
    _inherit = "purchase.request.line.make.purchase.order.item"

    product_qty = fields.Float(string='Quantity to purchase',
                               digits=(14, 4),)
    is_project_insume = fields.Boolean()
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        )
    product_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',)
    subtotal = fields.Float(
        digits=(14, 4),)


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    @api.model
    def _prepare_item(self, line):
        res = super(
            PurchaseRequestLineMakePurchaseOrder, self)._prepare_item(line)
        res['is_project_insume'] = True
        return res

    @api.model
    def _check_valid_request_line(self, request_line_ids):
        for line in self.env['purchase.request.line'].browse(request_line_ids):

            if line.request_id.state != 'approved':
                raise exceptions.Warning(
                    _('Purchase Request %s is not approved') %
                    line.request_id.name)
            if line.purchase_state in ['purchase', 'done']:
                raise exceptions.ValidationError(
                    _('The purchase has already been completed \n \n'
                      'Line: %s \n Product: %s.') %
                    (line.request_id.name, line.product_id.name))
        return (
            super(PurchaseRequestLineMakePurchaseOrder, self).
            _check_valid_request_line(request_line_ids))

    @api.model
    def _prepare_purchase_order_line(self, po, item):
        res = (
            super(PurchaseRequestLineMakePurchaseOrder, self).
            _prepare_purchase_order_line(po, item))
        res['is_project_insume'] = item.is_project_insume
        res['taxes_id'] = [(6, 0, item.product_id.supplier_taxes_id.ids)]
        res['specifications'] = item.line_id.specifications
        return res
