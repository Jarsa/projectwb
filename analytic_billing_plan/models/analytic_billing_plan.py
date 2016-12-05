# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class AnalyticBillingPlan(models.Model):
    _name = 'analytic.billing.plan'
    _description = "Analytic Billing Plan"

    name = fields.Char()
    customer_id = fields.Many2one(
        'res.partner', string="Customer", readonly=True)
    has_active_order = fields.Boolean(
        string='Billing request',
        help="Indicates that this billing plan line "
        "contains at least one non-cancelled billing request.",
        default=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        default='draft')
    quantity = fields.Float()
    price_unit = fields.Float("Price Unit")
    invoice_id = fields.Many2one('account.invoice')
    date = fields.Date('Date', required=True, default=fields.Date.today)
    amount = fields.Float(
        string='Amount', required=True,
        help=('Calculated by multiplying the quantity '
              'and the price given in the Product\'s '
              'cost price. Always expressed in the '
              'company main currency.'))
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    account_id = fields.Many2one('account.account', 'Account')
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        readonly=True)
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    task_id = fields.Many2one('project.task', string='Concept')
    ref = fields.Char()
    project_id = fields.Many2one(
        'project.project',
        string='Project')
    move_id = fields.Many2one('account.move', string='Account Move')

    @api.multi
    def action_button_confirm(self):
        for rec in self:
            account_move_obj = self.env['account.move']
            if not self.env.user.company_id.bridge_account_id:
                raise ValidationError(
                    _('You must have a bridge account assigned'
                        ' in the company configurations.'))
            if rec.amount < 0:
                raise ValidationError(
                    _('The amount must be higher than zero.'))
            total = rec.currency_id.compute(
                rec.amount,
                self.env.user.currency_id)
            accounts = {'credit': rec.account_id.id,
                        'debit': self.env.user.company_id.bridge_account_id.id}
            move_lines = []
            for name, account in accounts.items():
                move_line = (0, 0, {
                    'name': rec.name,
                    'account_id': account,
                    'narration': rec.ref,
                    'debit': (total if name == 'debit' else 0.0),
                    'credit': (total if name == 'credit' else 0.0),
                    'journal_id': 1,
                    'analytic_account_id': rec.account_analytic_id.id,
                    'project_id': rec.project_id.id,
                    'task_id': rec.task_id.id,
                    'partner_id': rec.project_id.partner_id.id,
                })
                move_lines.append(move_line)
            move = {
                'date': fields.Date.today(),
                'journal_id': 1,
                'name': _('Billing Request: %s') % (rec.name),
                'line_ids': [line for line in move_lines],
            }
            move_id = account_move_obj.create(move)
            rec.write({
                'state': 'confirm',
                'move_id': move_id.id,
                })

    @api.multi
    def action_button_draft(self):
        for rec in self:
            if rec.invoice_id.state == 'paid':
                raise ValidationError(
                    _('You can not delete a billing request'
                      'with a paid invoice.'))
            rec.invoice_id.unlink()
            rec.move_id.unlink()
            rec.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('billing.request')
        return super(AnalyticBillingPlan, self).create(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.invoice_id:
                raise ValidationError(
                    _('You can not delete a billing request'
                      'with invoice'))
            else:
                return super(AnalyticBillingPlan, self).unlink()
