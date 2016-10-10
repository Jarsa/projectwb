# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, exceptions, fields, models


class WizardBillingPlan(models.TransientModel):
    _name = 'wizard.billing.plan'
    _inherit = 'project.wbs_element'

    remaining_quantity = fields.Float(compute='_compute_remaining_quantity')
    wbs_element = fields.Many2one('project.wbs_element')

    @api.depends('quantity', 'quantity_invoice')
    def _compute_remaining_quantity(self):
        for rec in self:
            rec.remaining_quantity = rec.quantity - rec.quantity_invoice
            if rec.remaining_quantity < 0.0:
                raise exceptions.ValidationError(
                    _('The quantity to invoice must be less than'
                        'the remaining quantity'))

    @api.multi
    def create_billing(self):
        for rec in self:
            billing = self.env['analytic.billing.plan']
            if rec.quantity == rec.quantity_invoice:
                ref = _(
                    "Total Billing of: %s %s" % (
                        rec.quantity_invoice,
                        rec.product_id.product_uom_id.name))
                active_order = False
                rec.wbs_element.write({'quantity': 0.0})
            if rec.quantity_invoice < rec.quantity:
                ref = _(
                    "Partial Billing of: %s %s" % (
                        rec.quantity_invoice,
                        rec.product_id.product_uom_id.name))
                active_order = True
                rec.wbs_element.write({'quantity': rec.remaining_quantity})
            general_account = self.env['account.analytic.account'].search(
                [('name', '=', rec.project_id.name)])
            analytic_billing = billing.create({
                "account_id": rec.analytic_account_id.id,
                "customer_id": rec.project_id.partner_id.id,
                "date": fields.Date.today(),
                "name": rec.name,
                "product_id": rec.product_id.id,
                "unit_amount": rec.remaining_quantity,
                "price_unit": rec.product_id.unit_price,
                "amount_currency": -(
                    rec.product_id.unit_price * rec.quantity_invoice),
                "product_uom_id": rec.product_id.product_uom_id.id,
                "version_id": rec.project_id.version_id.id,
                "currency_id": self.env.user.company_id.currency_id.id,
                "quantity": rec.remaining_quantity,
                "concept": rec.id,
                "amount": (
                    rec.product_id.unit_price * rec.quantity_invoice),
                "company_id": self.env.user.company_id.id,
                "ref": ref,
                "general_account_id": general_account.id,
                "has_active_order": active_order,
            })
            rec.analytic_billing_id = analytic_billing.id

    @api.model
    def default_get(self, field):
        record_id = self.env.context['active_ids'][0]
        plan = self.env['project.wbs_element'].search(
            [('id', '=', record_id)])
        res = super(WizardBillingPlan, self).default_get(field)
        res.update(
            {
                'product_id': plan.product_id.id,
                'project_id': plan.project_id.id,
                'analytic_account_id': plan.analytic_account_id.id,
                'quantity': plan.quantity,
                'remaining_quantity': plan.remaining_quantity,
                'name': plan.name,
                'wbs_element': plan.id
            }
        )
        return res
