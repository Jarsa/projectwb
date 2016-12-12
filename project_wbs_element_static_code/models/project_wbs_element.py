# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import models
from openerp.osv import fields as old_fields


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    _columns = {
        'code': old_fields.char(),
        }

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The code of the WBS Element must be unique.')]
