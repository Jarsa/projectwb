# -*- coding: utf-8 -*-
# Copyright <2012> <Israel Cruz Argil, Argil Consulting>
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, exceptions, fields, models


class WizardBillingPlan(models.TransientModel):
    _name = 'wizard.billing.plan'

    item_ids = fields.One2many(
        'wizard.billing.plan.line',
        'billing_request_id', string='Items')

    @api.model
    def _prepare_item(self, line):
        return {
            'project_task': line['project_task'],
            'remaining_quantity': line['remaining_quantity'],
            'unit_price': line['unit_price'],
            'qty': line['qty'],
        }

    @api.model
    def default_get(self, fields):
        res = super(WizardBillingPlan, self).default_get(
            fields)
        project_task_obj = self.env['project.task']
        billing_line_ids = self.env.context['active_ids'] or []
        active_model = self.env.context['active_model']
        if not billing_line_ids:
            return res
        assert active_model == 'project.task', \
            'Bad context propagation'

        items = []
        control = 0
        project_validator = False
        state_validator = False
        for line in project_task_obj.browse(billing_line_ids):
            if control == 0:
                old_project = line.project_id.id
                current_project = line.project_id.id
                control = 1
            else:
                current_project = line.project_id.id
            if old_project != current_project:
                project_validator = True
            elif line.state != 'confirm':
                state_validator = True
            else:
                old_project = line.project_id.id
                lines = line.line_billing_ids.search(
                    [('task_id', '=', line.id)])
                res = super(WizardBillingPlan, self).default_get(fields)
                if len(lines) == 0:
                    quantity = line.qty
                else:
                    for billing in lines:
                        if billing.has_active_order:
                            if line.remaining_quantity > 0:
                                quantity = line.remaining_quantity
                            else:
                                quantity = line.qty
                        else:
                            raise exceptions.ValidationError(
                                _('The quantity to invoice is zero.'))
                line = {
                    'unit_price': line.unit_price,
                    'remaining_quantity': line.remaining_quantity,
                    'project_task': line.id,
                    'qty': quantity,
                }
                items.append([0, 0, self._prepare_item(line)])

        if project_validator:
            raise exceptions.ValidationError(
                _('The resources must be for the same project.'))
        elif state_validator:
            raise exceptions.ValidationError(
                _('The concept must be confirmed \n \n'
                    'Concept: %s.') %
                (line.name))

        res['item_ids'] = items
        return res

    @api.multi
    def create_billing(self):
        for rec in self:
            for item in rec.item_ids:
                if item.remaining_quantity < 0.0:
                    raise exceptions.ValidationError(
                        _('The quantity to invoice must be less than'
                            'the remaining quantity'))
                if item.project_task.state != 'confirm':
                    raise exceptions.ValidationError(
                        _('The concept must be confirmed.'))
                billing = self.env['analytic.billing.plan']
                if item.qty == item.quantity_invoice:
                    ref = _(
                        "Total Billing of: %s %s" % (
                            item.quantity_invoice,
                            item.project_task.uom_id.name))
                    active_order = False
                if item.quantity_invoice < item.qty:
                    ref = _(
                        "Partial Billing of: %s %s" % (
                            item.quantity_invoice,
                            item.project_task.uom_id.name))
                    active_order = True
                item.project_task.write(
                    {'remaining_quantity': item.remaining_quantity})
                billing.create({
                    "account_id": (
                        item.project_task.product_id.
                        property_account_income_id.id
                        if item.project_task.product_id.
                        property_account_income_id.id
                        else
                        item.project_task.product_id.
                        categ_id.property_account_income_categ_id.id),
                    "customer_id": item.project_task.project_id.partner_id.id,
                    "date": fields.Date.today(),
                    "name": item.project_task.name,
                    "price_unit": item.unit_price,
                    "product_uom_id": item.project_task.uom_id.id,
                    "currency_id": self.env.user.company_id.currency_id.id,
                    "quantity": item.quantity_invoice,
                    "task_id": item.project_task.id,
                    "amount": (
                        item.unit_price * item.quantity_invoice),
                    "company_id": self.env.user.company_id.id,
                    "ref": ref,
                    "account_analytic_id": (
                        item.project_task.analytic_account_id.id),
                    "has_active_order": active_order,
                    "project_id": item.project_task.project_id.id
                })
