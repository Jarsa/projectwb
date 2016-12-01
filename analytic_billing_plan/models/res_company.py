# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    bridge_account_id = fields.Many2one(
        'account.account',
        string="Bridge Account",
        help="Account for the account moves generated "
        "by billing request confirmations",)
