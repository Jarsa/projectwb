# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AnalyticBillingPlan(models.Model):
    _name = 'analytic.billing.plan'
    _description = "Analytic Billing Plan"
    _inherit = ['mail.thread']

    name = fields.Char()
    customer_id = fields.Many2one(
        'res.partner', string="Customer", readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='State',
        default='draft')
    date = fields.Date('Date', required=True, default=fields.Date.today)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    project_id = fields.Many2one(
        'project.project',
        string='Project')
    analytic_billing_plan_line_ids = fields.One2many(
        'analytic.billing.plan.line',
        'analytic_billing_plan_id',
        string="Analytic Billing Plan Lines",
        readonly=True, )
    invoice_id = fields.Many2one(
        'account.invoice',
        string="Invoice",)

    @api.multi
    def action_button_confirm(self):
        for rec in self:
            if not self.env.user.company_id.billing_request_journal_id:
                raise ValidationError(
                    _('You must have an account journal for the moves assigned'
                        ' in the company configurations.'))
            for line in rec.analytic_billing_plan_line_ids:
                if line.amount < 0:
                    raise ValidationError(
                        _('The amount must be higher than zero.'))
            rec.write({
                'state': 'confirm',
                })
            rec.message_post(
                _('<strong>Billing Request Confirmed.</strong><ul>'
                  '<li><strong>Confirmed by: </strong>%s</li>'
                  '<li><strong>Confirmed at: </strong>%s</li>'
                  '</ul>') % (self.env.user.name, fields.Datetime.now()))

    @api.multi
    def action_button_draft(self):
        for rec in self:
            if rec.state == 'paid':
                raise ValidationError(
                    _('You can not delete a billing request'
                      'with a paid invoice.'))
            for line in rec.analytic_billing_plan_line_ids:
                line.move_id.unlink()
                line.write({'state': 'draft', })
            rec.write({'state': 'draft'})
            rec.message_post(
                _('<strong>Billing Request Drafted.</strong><ul>'
                  '<li><strong>Confirmed by: </strong>%s</li>'
                  '<li><strong>Confirmed at: </strong>%s</li>'
                  '</ul>') % (self.env.user.name, fields.Datetime.now()))

    @api.model
    def prepare_invoice(self, project, partner, invoice, invoice_names, lines):
        return {
            'project_id': project.id,
            'partner_id': partner,
            'date_invoice': fields.Date.today(),
            'fiscal_position_id': (
                project.partner_id.property_account_position_id.id),
            'reference': invoice.ref,
            'name': invoice_names,
            'currency_id': invoice.analytic_billing_plan_id.currency_id.id,
            'payment_term_id': (
                project.partner_id.property_payment_term_id.id),
            'account_id': (
                project.partner_id.property_account_receivable_id.id),
            'type': 'out_invoice',
            'invoice_line_ids': [line for line in lines],
        }

    @api.multi
    def make_project_invoices(self):
        total = 0.0
        lines = []
        for rec in self:
            if rec.invoice_id:
                raise ValidationError(
                    _('The billing request already has an invoice.'))
            if rec.state != 'confirm':
                raise ValidationError(
                    _('The billing request must be confirmed.'))
            partner = rec.customer_id.id
            project = rec.project_id
            currency = rec.currency_id
            account = rec.analytic_billing_plan_line_ids[0].account_analytic_id
            invoice_names = ', '.join(
                rec.analytic_billing_plan_line_ids.mapped('name'))
            for invoice in rec.analytic_billing_plan_line_ids:
                total += currency.compute(
                    invoice.amount, self.env.user.currency_id)

            if total > 0.0:
                product = self.env.user.company_id.product_id
                lines.append(
                    (0, 0, {
                        'product_id': product.id,
                        'quantity': 1.0,
                        'price_unit': total,
                        'account_analytic_id': account.id,
                        'uom_id': self.env.ref(
                            'product.product_uom_unit').id,
                        'name': project[0].name + _(' Payment'),
                        'invoice_line_tax_ids': [(6, 0, [
                            x.id for x in product.taxes_id])],
                        'account_id': (
                            product.property_account_income_id.id or
                            product.categ_id.
                            property_account_income_categ_id.id),
                    }))

            invoice_id_create = self.env['account.invoice'].create(
                self.prepare_invoice(
                    project, partner, invoice, invoice_names, lines))
            rec.invoice_id = invoice_id_create.id

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

    @api.model
    def create(self, vals):
        res = super(AnalyticBillingPlan, self).create(vals)
        res.name = self.env.ref(
            'analytic_billing_plan.billing_request_sequence').next_by_id()
        count = 1
        for line in res.analytic_billing_plan_line_ids:
            line.name = self.assign_code(res, count)
            count += 1
        return res

    @api.model
    def assign_code(self, br, count):
        name = br.name + '-' + str(count)
        return name

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.invoice_id:
                raise ValidationError(
                    _('The Billing Request already has an invoice.'))
            rec.analytic_billing_plan_line_ids.unlink()
            return super(AnalyticBillingPlan, self).unlink()
