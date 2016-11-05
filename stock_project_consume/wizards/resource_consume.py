# -*- coding: utf-8 -*-0
# <2016> <Jarsa Sistemas, S.A. de C.V.>
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
            'qty_on_hand': line.qty_on_hand,
            'qty_to_consume': 1.0,
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
        control = 0
        project_validator = False
        for line in resource_line_obj.browse(resource_line_ids):
            if control == 0:
                old_project = line.task_resource_id.project_id.id
                current_project = line.task_resource_id.project_id.id
                control = 1
            else:
                current_project = line.task_resource_id.project_id.id
            if old_project != current_project:
                project_validator = True
            else:
                old_project = line.task_resource_id.project_id.id
                items.append([0, 0, self._prepare_item(line)])

        if project_validator:
            raise exceptions.ValidationError(
                _('The resources must be for the same project.'))
        res['item_ids'] = items
        return res

    @api.multi
    def make_consume(self):
        stock_picking_obj = self.env['stock.picking']
        moves = []
        for item in self.item_ids:
            if item.qty_to_consume > item.qty_on_hand:
                raise exceptions.ValidationError(
                    _('The quantity to consume must be lower or equal'
                        ' than the quantity on hand. Please check your data.'))
            if not item.line_id.task_resource_id.project_id.picking_out_id:
                raise exceptions.ValidationError(
                    _('The project must have a picking type for the consume.'))
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
                'account_analytic_id': item.analytic_account_id.id,
                'project_id': item.line_id.task_resource_id.project_id.id,
                'task_id': item.line_id.task_resource_id.id,
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
