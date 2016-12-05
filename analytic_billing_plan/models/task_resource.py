# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import _, api, exceptions, fields, models


class TaskResource(models.Model):
    _inherit = 'project.task'

    line_billing_ids = fields.One2many('analytic.billing.plan', 'task_id')
    nbr_billing = fields.Float(
        string="Billing Request",
        compute="_compute_nrb_billing")
    remaining_quantity = fields.Float(default=0.0)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    billing_task_total = fields.Float(
        string='Billing Total',
        compute='_compute_billing_total')
    product_id = fields.Many2one(
        'product.product',
        string='Product to Billing',
        domain=[('sale_ok', '=', True),
                ('type', '=', 'service')],
        )

    @api.multi
    def _compute_billing_total(self):
        for rec in self:
            invoices = self.env['account.invoice'].search([
                ('project_id', '=', rec.project_id.id),
                ('state', '=', 'paid'),
                ('type', '=', 'out_invoice')])
            if invoices:
                for invoice in invoices:
                    for line in invoice.invoice_line_ids:
                        if line.concept_id.id == rec.id:
                            rec.billing_task_total += line.price_subtotal
            else:
                rec.billing_task_total = 0.0

    @api.depends('line_billing_ids')
    def _compute_nrb_billing(self):
        for record in self:
            record.nbr_billing = len(record.line_billing_ids.search(
                [('task_id', '=', record.id)]))

    @api.multi
    def action_button_draft(self):
        for rec in self:
            if rec.nbr_billing > 0.0:
                raise exceptions.ValidationError(
                    _("You can't reset the concept because"
                        " it already has a billing request."))
        return super(TaskResource, self).action_button_draft()

    @api.multi
    def request_billing_request(self):
        return {
            'name': 'Billing Request',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.billing.plan',
            'domain': [(
                'account_analytic_id', '=', self.analytic_account_id.id)],
            'type': 'ir.actions.act_window',
        }
