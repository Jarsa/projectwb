# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Account Hierarchy",
    "summary": "This module add a parent on the analytic accounts",
    "version": "9.0.1.0.0",
    "category": "Hidden",
    "website": "https://www.jarsa.com.mx/",
    "author": "Jarsa Sistemas",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        'account', 'analytic'
    ],
    "data": [
        'views/account_analytic_account_view.xml',
    ],
}
