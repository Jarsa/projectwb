# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas S.A. de C.V.

from openerp import fields, models


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    date_start = fields.Date(default=fields.Date.today,)
    date_end = fields.Date(default=fields.Date.today,)
