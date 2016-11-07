# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime
from openerp import api, fields, models


class PurchaseRequest(models.TransientModel):

    _name = 'purchase.request.wizard'
    _description = 'Request for quotation wizard'

    item_ids = fields.One2many(
        'purchase.request.line.wizard',
        'wiz_id', string='Items')

    @api.model
    def _prepare_item(self, line):
        return {
            'line_id': line.id,
            'analytic_account_id': line.account_id.id,
            'product_id': line.product_id.id,
            'description': line.description,
            'uom_id': line.uom_id.id,
            'qty': line.qty,
        }

    @api.model
    def default_get(self, fields):
        res = super(PurchaseRequest, self).default_get(
            fields)
        resource_line_obj = self.env['analytic.resource.plan.line']
        resource_line_ids = self.env.context['active_ids'] or []
        active_model = self.env.context['active_model']

        if not resource_line_ids:
            return res
        assert active_model == 'analytic.resource.plan.line', \
            'Bad context propagation'

        items = []
        # self._check_valid_request_line(resource_line_ids)
        for line in resource_line_obj.browse(resource_line_ids):
            items.append([0, 0, self._prepare_item(line)])
        res['item_ids'] = items
        return res

    @api.multi
    def make_request(self):
        lines = []
        today = datetime.strptime(fields.Datetime.now(), "%Y-%m-%d %H:%M:%S")
        for item in self.item_ids:
            line = (0, 0, {
                'product_id': item.product_id.id,
                'name': item.description,
                'product_qty': item.qty_to_request,
                'date_required': today,
                'analytic_account_id': item.analytic_account_id.id,
                })
            lines.append(line)
        order = ({
            'company_id': self.env.user.company_id.id,
            'picking_type_id': 1,
            'requested_by': self.env.user.id,
            'name': self.env['purchase.request']._get_default_name(),
            'line_ids': lines,
            })
        purchase = self.env['purchase.request'].create(order)
        for item in self.item_ids:
            item.line_id.write({'purchase_request_ids': [(4, purchase.id)]})
        return {
            'name': 'Purchase Request',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.request',
            'res_id': purchase.id,
            'target': 'current',
            'type': 'ir.actions.act_window',
            }
