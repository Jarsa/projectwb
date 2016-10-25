# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class AccountInvoiceLine(models.Model):
    _description = "account"
    _inherit = 'account.invoice.line'

    concept_id = fields.Many2one('project.task', string="Concept")
