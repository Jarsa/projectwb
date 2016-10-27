from openerp import api, fields, models
from datetime import datetime, timedelta


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
        order = ({
            'company_id': self.env.user.company_id.id,
            'picking_type_id': 1,
            'requested_by': self.env.user.id,
            'name': self.env['purchase.request']._get_default_name(),
            'line_ids': [line for line in lines],
            })
        self.env['purchase.request'].create(order)
        # for active in active_ids:
        #         if not active.purchase_order_id:
        #             active.write({"purchase_order_id": order_id.id})
        #         for rec in active.child_ids:
        #             if rec.state == "confirm":
        #                 if not active.purchase_order_id:
        #                     rec.write({"purchase_order_id": order_id.id})
        return True
