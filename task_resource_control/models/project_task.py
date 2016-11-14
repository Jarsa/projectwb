# -*- coding: utf-8 -*-
# <2015> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"
    _name = "project.task"

    resource_control_ids = fields.One2many(
        'resource.control',
        'task_id',
        string='Resource change history')
