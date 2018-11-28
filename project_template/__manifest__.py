# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Project Template',
    'summary': 'Duplicate projects with WBS and Income',
    'version': '11.0.1.0.0',
    'category': 'Project',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project_wbs_element',
        'task_resource_billing',
        'project_billing_plan',
    ],
    'data': [
        'views/project_project.xml',
    ],
    'installable': True,
}
