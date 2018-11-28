# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def _prepare_income_ids(self):
        self.ensure_one()
        lines = []
        for rec in self.income_ids:
            lines.append((0, 0, {
                'income_type_id': rec.income_type_id,
                'name': rec.name,
                'qty': 1.0,
                'amount': 0.0,
            }))

    @api.multi
    def _create_child_wbs(self, parent_wbs):
        for wbs in parent_wbs.child_ids:
            wbs.create({
                'code': '%s copy' % wbs.code,
                'name': wbs.name,
                'description': wbs.description,
                'project_id': self.project_id.id,
                'parent_id': self.id
            })

    @api.multi
    def _create_wbs(self, base_proj):
        self.ensure_one()
        parent_wbs = base_proj.wbs_element_ids.filtered(
            lambda l: not l.parent_id)
        for wbs in parent_wbs:
            rec = wbs.create({
                'code': '%s copy' % wbs.code,
                'name': wbs.name,
                'description': wbs.description,
                'project_id': self.id,
            })
            if parent_wbs.child_ids:
                rec._create_child_wbs()

    @api.multi
    def duplicate_project(self):
        for rec in self:
            project = self.create({
                'name': '%s (Copy)' % rec.name,
                'income_ids': rec._prepare_income_ids()
            })
            project._create_wbs(rec)