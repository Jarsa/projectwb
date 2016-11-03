# -*- coding: utf-8 -*-0
# Copyright <2012> <Israel Cruz Argil, Argil Consulting>
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, exceptions, fields, models


class ResourceConsume(models.TransientModel):

    _name = 'resource.consume'
    _description = 'Make Product Consumes'

    item_ids = fields.One2many(
        'resource.consume.line',
        'wiz_id', string='Items')

    @api.model
    def _prepare_item(self, line):
        return {
            'line_id': line.id,
            'analytic_account_id': line.account_id.id,
            'product_id': line.product_id.id,
            'description': line.description or line.product_id.name,
            'uom_id': line.uom_id.id,
            'qty': line.qty,
            'qty_on_hand': line.qty_on_hand
        }

    @api.model
    def default_get(self, fields):
        res = super(ResourceConsume, self).default_get(
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
    def make_consume(self):
        stock_picking_obj = self.env['stock.picking']
        # stock_move_obj = self.env['stock.move']
        moves = []
        for item in self.item_ids:
            today = fields.Datetime.now()
            move = (0, 0, {
                'company_id': self.env.user.company_id.id,
                'date': today,
                'location_dest_id': (
                    item.line_id.task_resource_id.project_id.
                    picking_out_id.default_location_dest_id.id),
                'location_id': (
                    item.line_id.task_resource_id.project_id.
                    picking_out_id.default_location_src_id.id),
                'name': (item.product_id.name),
                'product_id': item.product_id.id,
                'product_uom': item.uom_id.id,
                'product_uom_qty': item.qty_to_consume,
                })
            moves.append(move)
        picking_dict = {
            'company_id': self.env.user.company_id.id,
            'move_lines': moves,
            'picking_type_id': (
                item.line_id.task_resource_id.project_id.
                picking_out_id.id),
            'location_dest_id': (
                item.line_id.task_resource_id.project_id.
                picking_out_id.default_location_dest_id.id),
            'location_id': (
                item.line_id.task_resource_id.project_id.
                picking_out_id.default_location_src_id.id),
        }
        picking = stock_picking_obj.create(picking_dict)
        return {
            'name': 'Picking',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'type': 'ir.actions.act_window'
            }
