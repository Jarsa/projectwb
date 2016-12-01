# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import _, api, exceptions, fields, models


class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    billing_project_total = fields.Float(
        'Billing Total',
        compute='_compute_billing_project_total',)
    project_amortization = fields.Integer(
        string='Project Amortization',)

    @api.multi
    @api.constrains('project_amortization')
    def _validate_percentage(self):
        for rec in self:
            if rec.project_amortization > 100 or rec.project_amortization < 0:
                raise exceptions.ValidationError(
                    _('The percentage value must be between 0 and 100.'))

    @api.multi
    def _compute_billing_project_total(self):
        for rec in self:
            wbs_elements = self.env['project.wbs_element'].search([
                ('project_id', '=', rec.id)])
            if wbs_elements:
                for wbs_element in wbs_elements:
                    rec.billing_project_total += (
                        wbs_element.billing_concept_total)
            else:
                rec.billing_project_total = 0.0
