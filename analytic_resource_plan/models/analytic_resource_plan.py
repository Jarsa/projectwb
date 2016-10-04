# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class AnalyticResourcePlanLine(models.Model):
    _name = 'analytic.resource.plan.line'
    _description = "Analytic Resource Planning lines"

    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account', required=True)
    name = fields.Char(
        string='Activity description', compute="_compute_product_id")
    date = fields.Date(
        required=True,
        compute="_compute_account_id")
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='Status',
        required=True, readonly=True,
        help=' * The \'Draft\' status is used when a user is encoding '
             'a new and unconfirmed resource plan line. '
             '\n* The \'Confirmed\' status is used for to confirm the '
             'execution of the resource plan lines.',
        default='draft')
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    product_uom_id = fields.Many2one(
        'product.uom', string='UoM', compute="_compute_product_id")
    unit_amount = fields.Float(
        string='Planned Quantity', readonly=True,
        required=True,
        help='Specifies the quantity that has been planned.',
        default=1)
    notes = fields.Text()
    parent_id = fields.Many2one(
        'analytic.resource.plan.line',
        string='Parent', readonly=True,)
    child_ids = fields.One2many(
        'analytic.resource.plan.line',
        'parent_id', string='Child lines')
    has_child = fields.Boolean(
        string="Child lines", compute="_compute_has_child")
    analytic_line_plan_ids = fields.One2many(
        'analytic.plan', 'resource_plan_id',
        string='Planned costs', readonly=True)

    @api.depends('account_id')
    def _compute_account_id(self):
        for line in self:
            if line.account_id:
                line.date = line.account_id.create_date

    @api.depends('product_id')
    def _compute_product_id(self):
        for line in self:
            if line.product_id:
                line.name = line.product_id.name
                line.product_uom_id = line.product_id.uom_id

    @api.depends('has_child')
    def _compute_has_child(self):
        for line in self:
            if line.child_ids:
                line.has_child = True

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        default['parent_id'] = False
        default['analytic_line_plan_ids'] = []
        return super(AnalyticResourcePlanLine, self).copy(default)

    @api.multi
    def prepare_analytic_lines(self):
        plan_version_obj = self.env['analytic.plan.version']
        for line in self:
            journal_id = (
                line.product_id.expense_analytic_plan_journal_id and
                line.product_id.expense_analytic_plan_journal_id.id or
                False)
            general_account_id = (
                line.product_id.property_account_expense_id.id)

            if not general_account_id:
                general_account_id = (
                    line.product_id.categ_id.
                    property_account_expense_categ_id.id)

            if not general_account_id:
                raise exceptions.ValidationError(
                    _('There is no expense account defined '
                      'for this product: "%s" (id:%d)')
                    % (line.product_id.name,
                       line.product_id.id,))

            default_plan_ids = plan_version_obj.search(
                [('default_resource_plan', '=', True)])

            if not default_plan_ids:
                raise exceptions.ValidationError(
                    _('No active planning version for resource plan exists.'))

            return [{
                'resource_plan_id': line.id,
                'account_id': line.account_id.id,
                'name': line.name,
                'date': line.date,
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom_id.id,
                'unit_amount': line.unit_amount,
                'amount': (-1 * line.product_id.standard_price *
                           line.unit_amount),
                'general_account_id': general_account_id,
                'journal_id': journal_id,
                'notes': line.notes,
                'version_id': default_plan_ids[0].id,
                'currency_id': line.account_id.company_id.currency_id.id,
                'amount_currency': (-1 * line.product_id.standard_price *
                    line.unit_amount),
            }]

    @api.multi
    def create_analytic_lines(self):
        res = []
        line_plan_obj = self.env['analytic.plan']
        lines_vals = self.prepare_analytic_lines()
        for line_vals in lines_vals:
            line_id = line_plan_obj.create(line_vals)
            res.append(line_id)
        return res

    @api.multi
    def delete_analytic_lines(self):
        for line in self:
            line_plan_obj = self.env['analytic.plan']
            ana_line_ids = line_plan_obj.search(
                [('resource_plan_id', '=', line.id)])
            ana_line_ids.unlink()

    @api.multi
    def action_button_draft(self):
        for line in self:
            line.delete_analytic_lines()
        return line.write({'state': 'draft'})

    @api.multi
    def action_button_confirm(self):
        for line in self:
            if not line.product_id.expense_analytic_plan_journal_id:
                raise exceptions.ValidationError(
                    _('The product should have a journal account.'))
            if line.unit_amount == 0:
                raise exceptions.ValidationError(
                    _('Quantity should be greater than 0.'))
            line.create_analytic_lines()
        return line.write({'state': 'confirm'})

    @api.multi
    def unlink(self):
        for line in self:
            child_ids = line.search([
                ('parent_id', '=', line.id),
                ('state', '=', 'confirm')])
            if child_ids:
                raise exceptions.ValidationError(
                    _('You cannot delete a resource plan line that is '
                      'parent to other resource plan lines that have been '
                      'confirmed!'))
            if line.analytic_line_plan_ids:
                raise exceptions.ValidationError(
                    _('You cannot delete a record that refers to analytic '
                      'plan lines!'))
        return super(AnalyticResourcePlanLine, self).unlink()
