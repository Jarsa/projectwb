# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project Image',
    'summary': 'Adds a default image to the project Kanban view',
    'version': '11.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Eficent Business and IT Consulting Services S.L.,'
        'Odoo Community Association (OCA), Jarsa Sistemas S.A. de C.V.'),
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': ['project'],
    'data': [
        'views/project_view.xml',
    ],
    'installable': True,
}
