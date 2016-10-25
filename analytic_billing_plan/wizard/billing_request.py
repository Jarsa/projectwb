# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, exceptions, fields, models


class WizardBillingPlan(models.TransientModel):
    _name = 'wizard.billing.plan'
    _inherit = 'project.task'

    remaining_quantity = fields.Float(
        compute='_compute_remaining_quantity')
    project_task = fields.Many2one('project.task')
    total_invoice = fields.Float(compute='_compute_total_invoice')

    @api.depends('quantity_invoice', 'unit_price')
    def _compute_total_invoice(self):
        for rec in self:
            rec.total_invoice = rec.quantity_invoice * rec.unit_price

    @api.depends('qty', 'quantity_invoice')
    def _compute_remaining_quantity(self):
        for rec in self:
            rec.remaining_quantity = rec.qty - rec.quantity_invoice
            if rec.remaining_quantity < 0.0:
                raise exceptions.ValidationError(
                    _('The quantity to invoice must be less than'
                        'the remaining quantity'))

    @api.multi
    def create_billing(self):
        for rec in self:
            billing = self.env['analytic.billing.plan']
            if rec.qty == rec.quantity_invoice:
                ref = _(
                    "Total Billing of: %s %s" % (
                        rec.quantity_invoice,
                        rec.uom_id.name))
                active_order = False
            if rec.quantity_invoice < rec.qty:
                ref = _(
                    "Partial Billing of: %s %s" % (
                        rec.quantity_invoice,
                        rec.uom_id.name))
                active_order = True
            rec.project_task.write(
                {'remaining_quantity': rec.remaining_quantity})
            general_account = self.env['account.analytic.account'].search(
                [('name', '=', rec.project_id.name)])
            billing.create({
                "account_id": (
                    rec.project_task.wbs_element_id.analytic_account_id.id),
                "customer_id": rec.project_id.partner_id.id,
                "date": fields.Date.today(),
                "name": rec.name,
                "product_id": rec.project_task.id,
                "price_unit": rec.unit_price,
                "amount_currency": -(
                    rec.unit_price * rec.quantity_invoice),
                "product_uom_id": rec.project_task.uom_id.id,
                "version_id": rec.project_id.version_id.id,
                "currency_id": self.env.user.company_id.currency_id.id,
                "quantity": rec.quantity_invoice,
                "concept": rec.id,
                "amount": (
                    rec.unit_price * rec.quantity_invoice),
                "company_id": self.env.user.company_id.id,
                "ref": ref,
                "general_account_id": general_account.id,
                "has_active_order": active_order,
            })

    @api.model
    def default_get(self, field):
        if 'active_id' in self.env.context:
            record_id = self.env.context['active_id']
            plan = self.env['project.task'].search(
                [('id', '=', record_id)])
            lines = plan.line_billing_ids.search(
                [('product_id', '=', plan.id)])
            res = super(WizardBillingPlan, self).default_get(field)
            res.update({
                'name': plan.name,
                'unit_price': plan.unit_price,
                'remaining_quantity': plan.remaining_quantity,
                'project_task': plan.id,
                'wbs_element_id': plan.wbs_element_id.id,
                'project_id': plan.project_id.id,
            })
            if len(lines) == 0:
                quantity = plan.qty
                res.update({'qty': quantity})
            else:
                for billing in lines:
                    if billing.has_active_order is True:
                        if plan.remaining_quantity > 0:
                            quantity = plan.remaining_quantity
                        else:
                            quantity = plan.qty
                        res.update({'qty': quantity})
                    else:
                        quantity = 0.0
                        res.update({'qty': quantity})
                        return res
            return res
        else:
            return super(WizardBillingPlan, self).default_get(field)
