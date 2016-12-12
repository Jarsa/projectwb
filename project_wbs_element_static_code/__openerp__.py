# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project WBS Element Static Code',
    'summary': 'The WBS Elements code must be assigned manually',
    'version': '9.0.1.0.0',
    'author': (
        'Jarsa Sistemas S.A. de C.V.,'
        'Odoo Community Association (OCA)'),
    'description': 'This module can assign the code',
    'website': 'https://www.odoo-community.org',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'depends': [
        'project_wbs_element'
    ],
    'data': [
        'views/project_wbs_element_view.xml',
    ],
    'installable': True,
}
