# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectIncomeType(models.Model):
    _name = 'project.income.type'

    name = fields.Char()
