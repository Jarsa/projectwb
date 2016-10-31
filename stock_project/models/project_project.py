# -*- coding: utf-8 -*-
# Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Project Location'
    )

    @api.model
    def create(self, vals):
        project = super(ProjectProject, self).create(vals)
        location = project.location_id.create({
            'name': self.env.user.company_id.name + '/' + project.name,
            'active': True,
            'partner_id': project.partner_id.id
        })
        project.location_id = location.id
        sequence_in_id = self.env['ir.sequence'].create({
            'name':  (
                self.env.user.company_id.name + ' ' +
                project.name + ' Sequence in'),
            'active': True,
            'implementation': 'no_gap',
            'prefix': 'WH/PRJ/IN/',
            'number_increment': 1
            })
        self.env['stock.picking.type'].create(
            {
                'name': location.name + '/Receptions',
                'sequence_id': sequence_in_id.id,
                'warehouse_id': 1,
                'code': 'incoming',
                'default_location_dest_id': location.id
            })
        return project
