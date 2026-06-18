# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ItEquipement(models.Model):
    _name = 'it.equipement'
    _description = 'Equipement informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'maintenance.equipment': 'maintenance_equipment_id'}
    _order = 'name, id'
    _check_company_auto = True

    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipement maintenance',
        required=True,
        ondelete='cascade',
        auto_join=True,
        index=True,
    )
    code = fields.Char(string='Reference interne', copy=False, tracking=True)
    asset_type = fields.Selection(
        [
            ('computer', 'Poste de travail'),
            ('server', 'Serveur'),
            ('printer', 'Imprimante'),
            ('network', 'Equipement reseau'),
            ('phone', 'Telephone IP'),
            ('license', 'Licence'),
            ('other', 'Autre'),
        ],
        string='Type',
        required=True,
        default='computer',
        tracking=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Brouillon'),
            ('assigned', 'Affecte'),
            ('maintenance', 'En maintenance'),
            ('retired', 'Retire'),
        ],
        string='Etat',
        required=True,
        default='draft',
        tracking=True,
    )
    employee_id = fields.Many2one('hr.employee', string='Employe affecte', tracking=True)
    department_id = fields.Many2one('hr.department', string='Departement', tracking=True)
    site = fields.Selection(
        [
            ('abidjan_cocody', 'Abidjan - Cocody'),
            ('abidjan_other', 'Abidjan - Autre site'),
            ('bouake', 'Bouake'),
        ],
        string='Site',
        default='abidjan_cocody',
        tracking=True,
    )
    purchase_order_id = fields.Many2one('purchase.order', string='Commande fournisseur')
    invoice_id = fields.Many2one('account.move', string='Facture fournisseur')
    purchase_date = fields.Date(string="Date d'achat", tracking=True)
    purchase_value = fields.Monetary(string="Valeur d'achat", currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    assignment_ids = fields.One2many('it.affectation', 'equipment_id', string='Historique des affectations')
    intervention_ids = fields.One2many('it.intervention', 'parc_equipment_id', string='Interventions')
    contract_ids = fields.Many2many(
        'it.contrat',
        'it_contrat_equipement_rel',
        'equipment_id',
        'contract_id',
        string='Contrats couvrant cet equipement',
    )
    alert_ids = fields.One2many('it.alerte', 'equipment_id', string='Alertes')
    assignment_count = fields.Integer(compute='_compute_counts', string="Nombre d'affectations")
    intervention_count = fields.Integer(compute='_compute_counts', string="Nombre d'interventions")
    alert_count = fields.Integer(compute='_compute_counts', string="Nombre d'alertes")
    warranty_days_left = fields.Integer(compute='_compute_warranty_days_left', string='Jours garantie', store=True)
    is_warranty_expired = fields.Boolean(compute='_compute_warranty_days_left', string='Garantie expiree', store=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'La reference interne doit etre unique.'),
    ]

    @api.depends('assignment_ids', 'intervention_ids', 'alert_ids')
    def _compute_counts(self):
        for equipment in self:
            equipment.assignment_count = len(equipment.assignment_ids)
            equipment.intervention_count = len(equipment.intervention_ids)
            equipment.alert_count = len(equipment.alert_ids)

    @api.depends('warranty_date')
    def _compute_warranty_days_left(self):
        today = fields.Date.context_today(self)
        for equipment in self:
            if equipment.warranty_date:
                equipment.warranty_days_left = (equipment.warranty_date - today).days
                equipment.is_warranty_expired = equipment.warranty_days_left < 0
            else:
                equipment.warranty_days_left = 0
                equipment.is_warranty_expired = False

    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        for equipment in self:
            if equipment.purchase_value < 0:
                raise ValidationError(_("La valeur d'achat ne peut pas etre negative."))

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for equipment in self:
            equipment.department_id = equipment.employee_id.department_id
            if equipment.employee_id and equipment.employee_id.user_id:
                equipment.owner_user_id = equipment.employee_id.user_id

    def action_assign(self):
        for equipment in self:
            if not equipment.employee_id:
                raise UserError(_("Selectionnez un employe avant d'affecter l'equipement."))
            equipment.state = 'assigned'
            equipment.assign_date = fields.Date.context_today(equipment)
            equipment._close_open_assignments()
            self.env['it.affectation'].create({
                'equipment_id': equipment.id,
                'employee_id': equipment.employee_id.id,
                'department_id': equipment.department_id.id,
                'date_start': fields.Date.context_today(equipment),
                'reason': _("Affectation initiale"),
            })

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})

    def action_retire(self):
        self.write({'state': 'retired', 'scrap_date': fields.Date.context_today(self)})
        self.mapped('assignment_ids').filtered(lambda assignment: assignment.state == 'active').action_close()

    def action_reset_draft(self):
        self.write({'state': 'draft'})

    def _close_open_assignments(self):
        self.mapped('assignment_ids').filtered(lambda assignment: assignment.state == 'active').action_close()
