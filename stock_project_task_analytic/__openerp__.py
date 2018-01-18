# -*- coding: utf-8 -*-
# 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock Project Task",
    "summary": "Adds an project task in stock move",
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.,"
    "Odoo Community Association (OCA), Jarsa Sistemas",
    "website": "https://www.odoo-community.org",
    "category": "Warehouse Management",
    "license": "AGPL-3",
    "depends": [
        "stock_analytic",
        "stock_project_analytic",
    ],
    "data": [
        "views/stock_move_views.xml",
        "views/stock_inventory_views.xml",
    ],
    'installable': True,
}
