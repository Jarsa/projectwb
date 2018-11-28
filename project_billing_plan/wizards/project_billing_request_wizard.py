# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProjectBillingRequestWizard(models.TransientModel):
    _name = 'project.billing.request.wizard'

    line_ids = fields.One2many('project.billing.request.wizard.line', 'wiz_id')
    project_id = fields.Many2one('project.project')

    @api.model
    def _prepare_item(self, line):
        return {
            'income_id': line.id,
            'name': line.name,
            'remaining_qty': line.remaining_qty,
            'qty': line.remaining_qty,
            'amount': line.amount,
        }

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        project = self.env['project.project'].browse(
            self._context.get('active_id'))
        lines = []
        for line in project.mapped('income_ids'):
            if line.remaining_qty <= 0:
                continue
            lines.append([0, 0, self._prepare_item(line)])
        res.update({
            'line_ids': lines,
            'project_id': self._context.get('active_id'),
        })
        return res

    @api.multi
    def create_billing(self):
        unit = self.env.ref('product.product_uom_unit')
        for rec in self:
            lines = []
            for line in rec.line_ids:
                ref = False
                active_order = False
                if line.qty == line.remaining_qty:
                    ref = _(
                        'Total Billing of: Project: %s - Quantity: %s') % (
                            self.project_id.name, line.qty)
                    active_order = False
                elif line.qty < line.remaining_qty:
                    ref = _(
                        'Partial Billing of: Project: %s - Quantity: %s') % (
                            self.project_id.name, line.qty)
                    active_order = True
                lines.append(
                    (0, 0,
                        {
                            'account_id': (
                                self.env.user.company_id.product_id.
                                property_account_income_id.id
                                if self.env.user.company_id.product_id.
                                property_account_income_id.id
                                else
                                self.env.user.company_id.product_id.
                                categ_id.property_account_income_categ_id.id),
                            'ref': ref,
                            'price_unit': line.amount,
                            'product_uom_id': unit.id,
                            'quantity': line.qty,
                            'income_id': line.income_id.id,
                            'amount': (
                                line.amount * line.qty),
                            'account_analytic_id': (
                                self.project_id.analytic_account_id.id),
                            'has_active_order': active_order,
                        })
                    )
            res = self.env['analytic.billing.plan'].create({
                'customer_id': self.project_id.partner_id.id,
                'date': fields.Date.today(),
                'project_id': self.project_id.id,
                'currency_id': self.env.user.company_id.currency_id.id,
                'analytic_billing_plan_line_ids': lines,
            })
            return {
                'name': _('Billing Request'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'analytic.billing.plan',
                'res_id': res.id,
                'target': 'current',
                'type': 'ir.actions.act_window',
            }


class ProjectBillingRequestWizardLine(models.TransientModel):
    _name = 'project.billing.request.wizard.line'

    wiz_id = fields.Many2one('project.billing.request.wizard')
    income_id = fields.Many2one('project.income')
    name = fields.Char()
    remaining_qty = fields.Float()
    amount = fields.Float()
    qty = fields.Float()
