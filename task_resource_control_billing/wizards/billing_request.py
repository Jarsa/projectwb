# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, exceptions, fields, models


class WizardBillingPlan(models.TransientModel):
    _inherit = 'wizard.billing.plan'

    qty = fields.Float(string='Planned Quantity',)
    real_qty = fields.Float(string='Real Quantity')

    @api.model
    def _prepare_item(self, line):
        res = super(WizardBillingPlan, self)._prepare_item(line)
        res['real_qty'] = line.real_qty
        return res

    @api.multi
    def create_billing(self):
        for rec in self:
            for item in rec.item_ids:
                if item.real_qty == item.quantity_invoice:
                    ref = _(
                        "Total Billing of: %s %s" % (
                            item.quantity_invoice,
                            item.project_task.uom_id.name))
                    active_order = False
                if item.quantity_invoice < item.real_qty:
                    ref = _(
                        "Partial Billing of: %s %s" % (
                            item.quantity_invoice,
                            item.project_task.uom_id.name))
                    active_order = True
            return super(WizardBillingPlan, self).create_billing()
