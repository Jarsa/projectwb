# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    wbs_element_id = fields.Many2one(
        'project.wbs_element',
        string='WBS Element')
    concept_id = fields.Many2one('project.task', string="Concept")
