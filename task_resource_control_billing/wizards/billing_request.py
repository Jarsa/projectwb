# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class WizardBillingPlan(models.TransientModel):
    _inherit = 'wizard.billing.plan'

    qty = fields.Float(string='Planned Quantity',)
    real_qty = fields.Float(string='Real Quantity')

    @api.model
    def _prepare_item(self, line):
        res = super(WizardBillingPlan, self)._prepare_item(line)
        res['real_qty'] = line['real_qty']
        return res
