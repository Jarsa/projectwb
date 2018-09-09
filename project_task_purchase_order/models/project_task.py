# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def show_purchase_order(self):
        return {
            'name': 'Purchase Order',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'purchase.order',
            'domain': [('task_id', '=', self.id)],
            'type': 'ir.actions.act_window',
        }
