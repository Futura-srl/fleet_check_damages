from odoo import fields, models, api
import logging


_logger = logging.getLogger(__name__)


class VehicleChecCamk(models.Model):
    _name = "fleet.check.cam"
    _description = "Fleet check cam"
    _inherit = "mail.thread"
    
    name = fields.Char(string="name")
    cam_code = fields.Char(string="Cam code")
    location = fields.Many2one('gtms.trip.type', string="Location")