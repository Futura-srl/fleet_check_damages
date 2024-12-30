from odoo import api, fields, models, _
from datetime import timedelta, datetime
from odoo.osv import expression
from odoo.exceptions import ValidationError


class TripType(models.Model):
    _inherit = 'gtms.trip.type'

    def _compute_count_trip_ready(self):
        for trip in self:
            trip.count_trip_ready = self.env['gtms.trip'].search_count(
                [('state', '!=', 'draft'), ('state', '!=', 'done'), ('state', '!=', 'cancel'), ('state', '!=', 'checked'),
                 ('trip_type_id', '=', trip.id)])


    def _compute_count_trip_late(self):
        for trip in self:
            now = datetime.now() + timedelta()
            trip.count_trip_late = self.env['gtms.trip'].search_count(
                [('state', '!=', 'done'), ('state', '!=', 'draft'), ('state', '!=', 'checked'), ('last_stop_planned_at', '<', now),
                 ('trip_type_id', '=', trip.id)])
