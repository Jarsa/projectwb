# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class ProjectProject(models.Model):
    _name = 'project.project'
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
