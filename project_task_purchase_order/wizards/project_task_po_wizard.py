# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models


class ProjectTaskPOWizard(models.TransientModel):
    _name = 'project.task.po.wizard'

    partner_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        domain=[('supplier', '=', True)],
        required=True)
    line_ids = fields.One2many(
        'project.task.po.wizard.line', 'wiz_id', string='Lines')

    @api.model
    def _prepare_item(self, line):
        return {
            'qty': line.qty,
            'uom_id': line.uom_id.id,
            'amount': line.unit_price,
            'name': line.name,
        }

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        tasks = self.env['project.task'].browse(
            self._context.get('active_ids'))
        lines = []
        for line in tasks:
            lines.append([0, 0, self._prepare_item(line)])
        res.update({
            'line_ids': lines,
        })
        return res

    @api.model
    def _prepare_po_line(self, line):
        return {
            'product_id': line.product_id.id,
            'name': line.name,
            'product_qty': line.qty,
            'price_unit': line.amount,
            'product_uom': line.uom_id.id,
            'date_planned': fields.Datetime.now()
        }

    @api.multi
    def create_purchase_order(self):
        for rec in self:
            lines = []
            for line in rec.line_ids:
                lines.append((0, 0, self._prepare_po_line(line)))
            res = self.env['purchase.order'].create({
                'partner_id': rec.partner_id.id,
                'order_line': lines,
                'date_planned': fields.Datetime.now()
            })
            return {
                'name': _('Purchase Order'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'purchase.order',
                'res_id': res.id,
                'target': 'current',
                'type': 'ir.actions.act_window',
            }


class ProjectTaskPOWizardLine(models.TransientModel):
    _name = 'project.task.po.wizard.line'

    wiz_id = fields.Many2one('project.task.po.wizard')
    name = fields.Char(required=True)
    product_id = fields.Many2one('product.product', required=True)
    qty = fields.Float(required=True)
    uom_id = fields.Many2one('product.uom', required=True)
    amount = fields.Float(required=True)
