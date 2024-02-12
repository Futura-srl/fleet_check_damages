from odoo import fields, models, api
import logging


_logger = logging.getLogger(__name__)


class VehicleCheck(models.Model):
    _name = "fleet.check"
    _description = "Fleet check"
    _inherit = "mail.thread"
    
    
    state = fields.Selection([('new','New'),('damages','With Damages'),('done','No Damages')], default='new')
    damage = fields.Char()
    fleet_check_photo_1_id = fields.Many2one('ir.attachment', string="Foto 1")
    fleet_check_photo_2_id = fields.Many2one('ir.attachment', string="Foto 2")
    fleet_check_photo_3_id = fields.Many2one('ir.attachment', string="Foto 3")
    fleet_check_photo_4_id = fields.Many2one('ir.attachment', string="Foto 4")
    fleet_check_photo_5_id = fields.Many2one('ir.attachment', string="Foto 5")
    fleet_check_photo_6_id = fields.Many2one('ir.attachment', string="Foto 6")
    fleet_check_photo_7_id = fields.Many2one('ir.attachment', string="Foto 7")
    fleet_check_photo_8_id = fields.Many2one('ir.attachment', string="Foto 8")
    
    
# class VehicleCheckPhoto(models.Model):
#     _name = "fleet.check.photo"
#     _description = "Fleet check photo"
    
    
#     name = fields.Char()
#     attachment_id = fields.Many2one('ir.attachment')
    
