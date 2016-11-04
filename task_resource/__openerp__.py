# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Task Resource',
    'summary': 'Task Resource',
    'version': '9.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Eficent Business and IT Consulting Services S.L.,'
        'Odoo Community Association (OCA)'),
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'product',
        'project_wbs_element',
        'purchase_request_to_rfq',
        ],

    'data': [
        'security/ir.model.access.csv',
        'wizards/purchase_request.xml',
        'views/total_task_resource_view.xml',
        'views/task_resource.xml',
    ],
    'installable': True,
}
