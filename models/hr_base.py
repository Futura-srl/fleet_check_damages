# from odoo import models, fields, api


# class HrEmployeeBase(models.AbstractModel):
#     _inherit = 'hr.employee.base'

#     related_contact_ids = fields.Many2many('res.partner', 'Related Contacts', compute='_compute_related_contacts')

#     # @api.depends('work_contact_id')
#     # def _compute_related_contacts(self):
#     #     for employee in self:
#     #         employee.related_contact_ids = employee.work_contact_id