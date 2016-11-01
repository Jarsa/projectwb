# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Stock Project',
    'summary': 'Stock Project',
    'version': '9.0.1.0.0',
    'description': 'This module allows the stock administration and'
                   'the consume of the products',
    'category': 'Generic Modules',
    'author': (
        'Jarsa Sistemas S.A. de C.V.'),
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'task_resource',
        ],

    'data': [
        'security/ir.model.access.csv',
        'views/analytic_resource_plan_view.xml',
        'views/project_project_view.xml',
        'wizards/resource_consume_view.xml'
    ],
    'installable': True,
}
