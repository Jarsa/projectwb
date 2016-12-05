# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Project Location',)
    picking_out_id = fields.Many2one(
        comodel_name='stock.picking.type',
        string='Picking Out',)
    picking_in_id = fields.Many2one(
        comodel_name='stock.picking.type',
        string='Picking In',)
    operations_state = fields.Boolean(
        compute='_compute_operations_state')

    @api.depends('state')
    @api.multi
    def _compute_operations_state(self):
        for rec in self:
            if rec.picking_out_id and rec.picking_in_id:
                if rec.state in ['close', 'cancelled']:
                    rec.picking_in_id.active = False
                    rec.picking_out_id.active = False
                    rec.operations_state = False
                else:
                    rec.picking_in_id.active = True
                    rec.picking_out_id.active = True
                    rec.operations_state = True
