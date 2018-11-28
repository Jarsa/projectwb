# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Project Control Billing',
    'summary': 'Project Control Billing',
    'version': '11.0.1.0.0',
    'category': 'Project',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'analytic_billing_plan',
    ],
    'data': [
        'views/project_project.xml',
        'views/project_income_type.xml',
        'wizards/project_billing_request_wizard.xml',
    ],
    'installable': True,
}
