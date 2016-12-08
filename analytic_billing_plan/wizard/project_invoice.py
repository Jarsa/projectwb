# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class ProjectInvoice(models.TransientModel):

    """ To create payment for invoice"""

    _name = 'project.invoice'
    _description = 'Make Payment for Concepts'

    @api.multi
    def make_project_invoices(self):
        active_ids = self.env['analytic.billing.plan'].browse(
            self._context.get('active_ids'))
        if not active_ids:
            return {}

        partner_ids = []
        project_ids = []
        total = 0.0
        invoice_names = ''
        control = 0
        control_project = 0
        lines = []

        for invoice in active_ids:
            if len(invoice.invoice_id) > 0:
                raise exceptions.ValidationError(
                    _('The billing request already has an invoice'))
            if (invoice.state in ('confirm')):
                partner = invoice.customer_id.id
                partner_ids.append(partner)
                project = invoice.project_id
                task = invoice.task_id
                project_ids.append(project)
                currency = invoice.currency_id
                total += currency.compute(
                    invoice.amount, self.env.user.currency_id)
                invoice_names += ' ' + invoice.name + ', '
            else:
                raise exceptions.ValidationError(
                    _('The invoices must be in confirmed / closed state'
                      ' and unpaid.'))

        for partner_id in partner_ids:
            if control == 0:
                old_partner = partner_id
                current_partner = partner_id
                control = 1
            else:
                current_partner = partner_id
            if old_partner != current_partner:
                raise exceptions.ValidationError(
                    _('The invoices must be of the same customer. '
                      'Please check it.'))
            else:
                old_partner = partner_id

        for project_id in project_ids:
            if control_project == 0:
                old_project = project_id.id
                current_project = project_id.id
                control_project = 1
            else:
                current_project = project_id.id
            if old_project != current_project:
                raise exceptions.ValidationError(
                    _('The invoices must be of the same project. '
                      'Please check it.'))
            else:
                old_project = project_id.id

        if total > 0.0:
            lines.append(
                (0, 0, {
                    'product_id': self.env.ref(
                        'analytic_billing_plan.product_concept').id,
                    'quantity': 1.0,
                    'price_unit': total,
                    'uom_id': self.env.ref('product.product_uom_unit').id,
                    'name': project.name + _(' Payment'),
                    'invoice_line_tax_ids': [(6, 0, [
                        x.id for x in task.product_id.taxes_id])],
                    'account_id': (
                        self.env.user.company_id.bridge_account_id.id),
                }))

            if project.project_amortization > 0:
                product_amortization = self.env.ref(
                    'analytic_billing_plan.'
                    'product_amortization')
                if len(product_amortization) == 0:
                    raise exceptions.ValidationError(
                        _('You must have a product for project '
                            'amortizations.'))
                product_account = (
                    product_amortization.property_account_expense_id
                    if product_amortization.property_account_expense_id
                    else product_amortization.categ_id.
                    property_account_expense_categ_id
                    if product_amortization.categ_id.
                    property_account_expense_categ_id
                    else False)
                if not product_account:
                    raise exceptions.ValidationError(
                        _('You must have an account for the product'))
                percentage_rate = float(project.project_amortization) / 100
                lines.append(
                    (0, 0, {
                        'product_id': product_amortization.id,
                        'quantity': 1.0,
                        'price_unit': (total * percentage_rate) * -1.0,
                        'name': project.name + _(' Amortization'),
                        'invoice_line_tax_ids': [(6, 0, [
                            x.id for x in task.product_id.taxes_id])],
                        'account_id': product_account.id,
                    }))

        invoice_id_create = self.env['account.invoice'].create({
            'project_id': project.id,
            'partner_id': project.partner_id.id,
            'date_invoice': fields.Date.today(),
            'fiscal_position_id': (
                project.partner_id.property_account_position_id.id),
            'reference': invoice.ref,
            'currency_id': invoice.currency_id.id,
            'payment_term_id': project.partner_id.property_payment_term_id.id,
            'account_id': (
                project.partner_id.property_account_receivable_id.id),
            'type': 'out_invoice',
            'invoice_line_ids': [line for line in lines],
        })

        for invoice_create in active_ids:
            invoice_create.invoice_id = invoice_id_create.id

        return {
            'name': 'Customer Invoice',
            'view_id': self.env.ref(
                'account.invoice_form').id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'account.invoice',
            'res_id': invoice_id_create.id,
            'type': 'ir.actions.act_window'
        }
