# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime
from openerp import api, fields, models


class PurchaseRequest(models.TransientModel):

    _name = 'purchase.request.wizard'
    _description = 'Request for quotation wizard'

    @api.multi
    def make_request(self):
        active_ids = self.env['analytic.resource.plan.line'].browse(
            self._context.get('active_ids'))
        if not active_ids:
            return {}
        lines = []
        today = datetime.strptime(fields.Datetime.now(), "%Y-%m-%d %H:%M:%S")
        for active in active_ids:
            line = (0, 0, {
                'product_id': active.product_id.id,
                'name': active.product_id.name,
                'product_qty': active.qty,
                'date_required': today,
                'analytic_account_id': active.account_id.id,
                })
            lines.append(line)
        line_values = []
        for line in lines:
            line_values.append(line)
        order = ({
            'company_id': self.env.user.company_id.id,
            'picking_type_id': 1,
            'requested_by': self.env.user.id,
            'name': self.env['purchase.request']._get_default_name(),
            'line_ids': line_values,
            })
        self.env['purchase.request'].create(order)
        return True
