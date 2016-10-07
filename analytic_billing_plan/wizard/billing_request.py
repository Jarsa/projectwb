# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, models


class WizardBillingPlan(models.TransientModel):
    _name = 'wizard.billing.plan'
    _inherit = 'project.wbs_element'

    @api.model
    def default_get(self, field):
        record_id = self.env.context['active_ids'][0]
        plan = self.env['project.wbs_element'].search(
            [('id', '=', record_id)])
        res = super(WizardBillingPlan, self).default_get(field)
        res.update({'child_ids': plan.child_ids.ids})
        return res
