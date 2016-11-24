# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, models


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
                    _('The invoice already has an invoice'))
            else:
                if (invoice.state in ('confirm')):
                    partner = invoice.customer_id.id
                    partner_ids.append(partner)
                    project = invoice.project_id.id
                    project_ids.append(project)
                    currency = invoice.currency_id
                    total += currency.compute(
                        invoice.amount, self.env.user.currency_id)
                    invoice_names += ' ' + invoice.name + ', '
                else:
                    raise exceptions.ValidationError(
                        _('The invoices must be in confirmed / closed state'
                          ' and unpaid.'))
                if total > 0.0:
                    lines.append(
                        (0, 0, {
                            'concept_id': invoice.task_id.id,
                            'wbs_element_id': (
                                invoice.task_id.wbs_element_id.id),
                            'quantity': invoice.quantity,
                            'price_unit': invoice.price_unit,
                            'name': invoice.task_id.name,
                            'invoice_line_tax_ids': [(
                                6, 0,
                                [
                                    x.id for x in invoice.task_id.
                                    product_id.taxes_id]
                                )],
                            'account_id': (
                                invoice.task_id.product_id.
                                property_account_income_id.id),
                            'account_analytic_id': (
                                invoice.account_analytic_id.id)
                        }))

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
                old_project = project_id
                current_project = project_id
                control_project = 1
            else:
                current_project = project_id
            if old_project != current_project:
                raise exceptions.ValidationError(
                    _('The invoices must be of the same project. '
                      'Please check it.'))
            else:
                old_project = partner_id

        invoice_id_create = self.env['account.invoice'].create({
            'project_id': invoice.project_id.id,
            'partner_id': invoice.customer_id.id,
            'fiscal_position_id': (
                invoice.customer_id.property_account_position_id.id),
            'reference': invoice.ref,
            'currency_id': invoice.currency_id.id,
            'account_id': (
                invoice.customer_id.property_account_receivable_id.id),
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
