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
        total = 0.0
        invoice_names = ''
        control = 0
        lines = []
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

        for invoice in active_ids:
            if len(invoice.invoice_id) > 0:
                raise exceptions.ValidationError(
                    _('The invoice already has an invoice'))
            else:
                if (invoice.state in ('confirm')):
                    partner_address = invoice.customer_id.address_get(
                        ['invoice', 'contact']).get('invoice', False)
                    if not partner_address:
                        raise exceptions.ValidationError(
                            _('You must configure the home address for the'
                              ' Customer.'))
                    partner_ids.append(partner_address)
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
                            'concept_id': invoice.product_id.id,
                            'quantity': invoice.quantity,
                            'price_unit': invoice.price_unit,
                            'invoice_line_tax_ids': [(
                                6, 0,
                                [x.id for x in invoice.product_id.tax_ids]
                            )],
                            'name': invoice.product_id.name,
                            'account_id': invoice.product_id.
                            wbs_element_id.analytic_account_id.id,
                        }))

        invoice_id_create = self.env['account.invoice'].create({
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
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'account.invoice',
            'res_id': invoice_id_create.id,
            'type': 'ir.actions.act_window'
        }
