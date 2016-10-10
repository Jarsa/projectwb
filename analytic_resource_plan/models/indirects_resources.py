# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class IndirectsResources(models.Model):
    _name = 'indirects.resources'
    _description = 'Indirects Resources Model'
    _inherit = 'product.product'