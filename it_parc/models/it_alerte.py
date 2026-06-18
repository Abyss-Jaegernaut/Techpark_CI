# -*- coding: utf-8 -*-

from odoo import fields, models


class ItAlerte(models.Model):
    _name = 'it.alerte'
    _description = 'Alerte parc informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_deadline, id desc'
    _check_company_auto = True

    name = fields.Char(string='Objet', required=True, tracking=True)
    alert_type = fields.Selection(
        [('warranty', 'Garantie'), ('contract', 'Contrat'), ('maintenance', 'Maintenance'), ('other', 'Autre')],
        string='Type',
        required=True,
        default='warranty',
        tracking=True,
    )
    severity = fields.Selection(
        [('info', 'Information'), ('warning', 'Avertissement'), ('critical', 'Critique')],
        string='Severite',
        default='warning',
        required=True,
        tracking=True,
    )
    equipment_id = fields.Many2one('it.equipement', string='Equipement', ondelete='cascade', tracking=True)
    contract_id = fields.Many2one('it.contrat', string='Contrat', ondelete='cascade', tracking=True)
    company_id = fields.Many2one('res.company', string='Societe', default=lambda self: self.env.company, required=True)
    date_deadline = fields.Date(string='Echeance', required=True, tracking=True)
    message = fields.Text(string='Message')
    state = fields.Selection(
        [('open', 'Ouverte'), ('done', 'Traitee'), ('cancelled', 'Annulee')],
        string='Etat',
        default='open',
        required=True,
        tracking=True,
    )

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
