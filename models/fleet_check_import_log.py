from odoo import fields, models, api
from datetime import datetime
import logging


_logger = logging.getLogger(__name__)


class VehicleCheckImportLog(models.Model):
    _name = "fleet.check.import.log"
    _description = "Fleet check import log"
    _inherit = "mail.thread"
    
    name = fields.Char(string="name")
    cam_code = fields.Many2one('fleet.check.import.log')
    attachment_csv_id = fields.Many2one('ir.attachment')
    attachment_csv_datas = fields.Binary(compute="_compute_attachment_csv_datas")
    photo_name = fields.Char()
    datetime_photo = fields.Datetime()
    esito = fields.Boolean()
    cam_error = fields.Char()
    location_id = fields.Many2one('gtms.trip.type', string="Location")
    export_processed = fields.Boolean()
    export_error = fields.Char()



    @api.depends('attachment_csv_id')
    def _compute_attachment_csv_datas(self):
        for record in self:
            record.attachment_csv_datas = record.attachment_csv_id.datas if record.attachment_csv_id else False
    