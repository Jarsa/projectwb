# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    code = fields.Char(string='Task code')
