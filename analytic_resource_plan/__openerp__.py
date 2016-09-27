# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Analytic Resource Plan',
    'version': '9.0.1.0.0',
    'author': 'Jarsa Sistemas, S.A de C.V.',
    'description': 'This module is to analytic plan',
    'website': 'https://www.jarsa.com.mx',
    'license': 'AGPL-3',
    'depends': [
        'analytic_plan',
        'account',
    ],
    'data': [
        'analytic_resource_plan_view.xml',
        'product_view.xml',
        'project_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'active': False,
}
