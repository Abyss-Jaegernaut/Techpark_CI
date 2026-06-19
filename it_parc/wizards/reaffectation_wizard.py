# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class ItReaffectationWizard(models.TransientModel):
    _name = 'it.reaffectation.wizard'
    _description = "Assistant de reaffectation d'equipement"

    equipment_id = fields.Many2one('it.equipement', string='Equipement', required=True)
    current_employee_id = fields.Many2one(related='equipment_id.employee_id', string='Employe actuel', readonly=True)
    current_department_id = fields.Many2one(related='equipment_id.department_id', string='Departement actuel', readonly=True)
    new_employee_id = fields.Many2one('hr.employee', string='Nouvel employe', required=True)
    new_department_id = fields.Many2one('hr.department', string='Nouveau departement')
    date_start = fields.Date(string='Date de reaffectation', required=True, default=fields.Date.context_today)
    reason = fields.Text(string='Motif', required=True)

    def action_reassign(self):
        self.ensure_one()
        if self.equipment_id.state == 'retired':
            raise UserError(_("Un equipement retire ne peut pas etre reaffecte."))
        department = self.new_department_id or self.new_employee_id.department_id
        self.equipment_id._close_open_assignments()
        self.env['it.affectation'].create({
            'equipment_id': self.equipment_id.id,
            'employee_id': self.new_employee_id.id,
            'department_id': department.id,
            'date_start': self.date_start,
            'reason': self.reason,
        })
        return {'type': 'ir.actions.act_window_close'}
