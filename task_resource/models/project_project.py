# -*- coding: utf-8 -*-
# 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"
    _name = "project.project"

    resource_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Resource Control Sequence',
        required=True)
    resource_control_id = fields.One2many(
        'resource.control',
        'project_id',
        string="Resource controls")

    @api.model
    def create(self, values):
        res = super(ProjectProject, self).create(values)
        resource_sequence = self.env['ir.sequence'].create({
            'name':  res.name + '/ [Resource control]',
            'active': True,
            'implementation': 'no_gap',
            'prefix': res.name + '-RC-',
            'number_increment': 1
            })
        res.resource_sequence_id = resource_sequence
        return res
