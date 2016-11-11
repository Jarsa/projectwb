# -*- coding: utf-8 -*-0
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class ResourceControl(models.TransientModel):

    _name = 'resource.control.wizard'
    _description = 'Make Product Consumes'

    item_ids = fields.One2many(
        'resource.control.line',
        'wiz_id', string='Items')

    @api.model
    def _prepare_item(self, line, model):
        if model == 'project.task':
            dic = {
                'task_id': line.id,
                'uom_id': line.uom_id.id,
                'qty': line.qty,
                'unit_price': line.unit_price,
                'subtotal': line.subtotal,
                'description': line.description,
                'analytic_account_id': line.analytic_account_id.id
            }
        else:
            dic = {
                'line_id': line.id,
                'analytic_account_id': line.account_id.id,
                'product_id': line.product_id.id,
                'qty': line.qty,
                'description': line.description or line.product_id.name,
                'uom_id': line.uom_id.id
            }
        return dic

    @api.model
    def default_get(self, fields):
        res = super(ResourceControl, self).default_get(
            fields)
        active_model = self.env.context['active_model']
        active_obj = self.env[active_model]
        active_ids = self.env.context['active_ids'] or []

        if not active_ids:
            return res

        items = []
        for line in active_obj.browse(active_ids):
            items.append([0, 0, self._prepare_item(line, active_model)])
        res['item_ids'] = items
        return res

    @api.multi
    def make_control(self):
        for rec in self:
            for item in rec.item_ids:
                if not item.task_id:
                    project_id = item.line_id.task_resource_id.project_id.id
                    qty_planned = item.line_id.qty
                    analytic_account = item.line_id.account_id.id
                    item.line_id.write({'real_qty': item.new_qty})
                else:
                    project_id = item.task_id.project_id.id
                    qty_planned = item.task_id.qty
                    analytic_account = item.task_id.analytic_account_id.id
                    item.task_id.write({'qty': item.new_qty})
                if qty_planned > item.new_qty:
                    item.type = 'deductive'
                elif qty_planned < item.new_qty:
                    item.type = 'additive'
                else:
                    raise ValidationError(
                        _("The new quantity must be greather or "
                          "smaller than the planned quantity"))

                self.env['resource.control'].create({
                    'project_id': project_id,
                    'insume_explotion_id': item.line_id.id,
                    'task_id': item.task_id.id,
                    'type': item.type,
                    'analytic_account_id': analytic_account,
                    'new_qty': item.new_qty,
                    })
