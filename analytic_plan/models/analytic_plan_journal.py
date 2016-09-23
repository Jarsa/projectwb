# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models



class AnalyticPlanJournal(models.Model):

    _name = 'analytic.plan.journal'
    _description = 'Analytic Journal Plan'

    name = fields.Char(string='Planning Journal Name', required=True)
    code = fields.Char(string='Planning Journal Code')
    active = fields.Boolean(
        help="If the active field is set to False, "
             "it will allow you to hide the analytic "
             "journal without removing it.")
    type = fields.Selection(
        [('sale', 'Sale'),
         ('purchase', 'Purchase'),
         ('cash', 'Cash'),
         ('general', 'General'),
         ('situation', 'Situation')],
        required=True,
        help="Gives the type of the analytic "
             "journal. When it needs for a document "
             "(eg: an invoice) to create analytic "
             "entries, OpenERP will look  for a "
             "matching journal of the same type.")
    line_ids = fields.One2many(
        'analytic.plan', 'journal_id', string='Lines')
    company_id = fields.Many2one(
        'res.company', string='Company', required=True)
    analytic_journal = fields.Many2one(
        'account.journal', string='Actual Analytic journal',
        required=False)
