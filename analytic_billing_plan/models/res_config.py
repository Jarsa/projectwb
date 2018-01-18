# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectConfigSettings(models.TransientModel):
    _inherit = 'project.config.settings'

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id,
        required=True,)
    bridge_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Bridge Account",
        help="Account for the account moves generated "
        "by billing request confirmations",
        compute="_compute_bridge_account_id",
        inverse="_inverse_bridge_account_id",)
    billing_request_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Billing Request Journal",
        compute="_compute_billing_request_journal_id",
        inverse="_inverse_billing_request_journal_id",)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product to Billing',
        domain=[('sale_ok', '=', True),
                ('type', '=', 'service')],
        compute="_compute_product_id",
        inverse="_inverse_product_id",)

    @api.multi
    @api.depends('company_id')
    def _compute_bridge_account_id(self):
        for rec in self:
            rec.bridge_account_id = rec.company_id.bridge_account_id.id

    @api.multi
    def _inverse_bridge_account_id(self):
        for rec in self:
            if rec.bridge_account_id != rec.company_id.bridge_account_id:
                rec.company_id.bridge_account_id = rec.bridge_account_id.id

    @api.multi
    @api.depends('company_id')
    def _compute_billing_request_journal_id(self):
        for rec in self:
            rec.billing_request_journal_id = (
                rec.company_id.billing_request_journal_id.id)

    @api.multi
    def _inverse_billing_request_journal_id(self):
        for rec in self:
            if (rec.billing_request_journal_id !=
                    rec.company_id.billing_request_journal_id):
                rec.company_id.billing_request_journal_id = (
                    rec.billing_request_journal_id.id)

    @api.multi
    @api.depends('company_id')
    def _compute_product_id(self):
        for rec in self:
            rec.product_id = rec.company_id.product_id.id

    @api.multi
    def _inverse_product_id(self):
        for rec in self:
            if rec.product_id != rec.company_id.product_id:
                rec.company_id.product_id = rec.product_id.id
