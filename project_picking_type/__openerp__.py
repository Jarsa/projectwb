# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project Picking Type',
    'summary': 'Picking Type OUT/IN',
    'version': '9.0.1.0.0',
    'description': 'This module allows the creation of ubication for each'
    'project created in Odoo',
    'category': 'Generic Modules',
    'author': (
        'Jarsa Sistemas S.A. de C.V.'),
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'stock',
        'task_resource',
        ],
    'data': [
        'views/project_project_view.xml',
    ],
    'installable': True,
}
