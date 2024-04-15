from odoo import fields, models, api
import logging


_logger = logging.getLogger(__name__)



class Reparation(models.Model):
    _inherit = 'reparation.reparation'

    fleet_check_id = fields.Many2one('fleet.check')
    event_date = fields.Datetime(compute="_event_date_fleet_vehicle_log_services", string="Event Date")

    @api.depends('fleet_vehicle_log_service_id')
    def _event_date_fleet_vehicle_log_services(self):
        for record in self:
            event_datetime = record.fleet_vehicle_log_service_id.date
            _logger.info("STAMPO DATETIME EVENTO")
            record.event_date = event_datetime
            _logger.info(record.event_date)