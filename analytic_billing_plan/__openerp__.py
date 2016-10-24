# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Analytic Billing Plan',
    'version': '9.0.1.0.0',
    'author': (
        'Jarsa Sistemas, S.A de C.V., Odoo Community Association (OCA)'),
    'description': 'This module is to analytic billing plan',
    'website': 'https://www.jarsa.com.mx',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'depends': [
        'project_wbs_element',
        'account',
        'analytic_plan',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/analytic_billing_view.xml',
        'wizard/billing_request_view.xml',
        'views/project_wbs_element.xml',
    ],
    'installable': True,
    'active': True,
}
