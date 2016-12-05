# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_project_insume = fields.Boolean()

    @api.multi
    def _create_stock_moves(self, picking):
        moves = super(PurchaseOrderLine, self)._create_stock_moves(picking)
        for rec in self:
            if rec.account_analytic_id:
                for move in moves:
                    move.account_analytic_id = rec.account_analytic_id.id
                    move.project_id = rec.env['project.task'].search(
                        [(
                            'analytic_account_id', '=',
                            rec.account_analytic_id.id)]).project_id.id
                    move.task_id = rec.env['project.task'].search(
                        [(
                            'analytic_account_id', '=',
                            rec.account_analytic_id.id)]).id
        return moves
