# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product to Billing',
        domain=[('sale_ok', '=', True),
                ('type', '=', 'service')],
        compute="_get_product_id",
        inverse="_set_product_id",)
    billing_request_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal to Billing Plan',
        compute="_get_billing_request_journal_id",
        inverse="_set_billing_request_journal_id",)

    @api.multi
    @api.depends('company_id')
    def _get_product_id(self):
        for rec in self:
            rec.product_id = rec.company_id.product_id.id

    @api.multi
    def _set_product_id(self):
        for rec in self:
            if rec.product_id != rec.company_id.product_id:
                rec.company_id.product_id = rec.product_id.id

    @api.multi
    @api.depends('company_id')
    def _get_billing_request_journal_id(self):
        for rec in self:
            rec.billing_request_journal_id = (
                rec.company_id.billing_request_journal_id.id)

    @api.multi
    def _set_billing_request_journal_id(self):
        for rec in self:
            if (rec.billing_request_journal_id !=
                    rec.company_id.billing_request_journal_id):
                rec.company_id.billing_request_journal_id = (
                    rec.billing_request_journal_id.id)
