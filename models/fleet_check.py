from odoo import fields, models, api
import logging


_logger = logging.getLogger(__name__)


class VehicleCheck(models.Model):
    _name = "fleet.check"
    _description = "Fleet check"
    _inherit = "mail.thread"

    name = fields.Char()
    state = fields.Selection([('new','New'),('damages','With Damages'),('done','No Damages'),('old','Older')], default='new')
    damage_ids= fields.Many2many('fleet.damage.type', 'name')
    trip_id = fields.Many2one('gtms.trip', string="Trip")
    # damage_id = fields.Many2one('')
    # reparation_id = fields.Many2one('')

    # Campi relativi alle foto originali e non modificate dall'AI
    fleet_check_photo_id = fields.Many2one('ir.attachment', string="Foto")
    fleet_check_photo_datas = fields.Binary(string="Foto Datas", compute='_compute_fleet_check_photo_datas')
    fleet_check_photo_url = fields.Char(string="Foto Url", compute='_compute_fleet_check_photo_url')
    fleet_check_photo_state = fields.Many2one('')
    fleet_check_photo_cam_id = fields.Many2one('fleet.check.cam')
    # Campi relativi alle immagini del mezzo di eventuali danni di categoria ancora in stato aperto
    last_trip_fleet_check_photo_id = fields.Many2one('ir.attachment', string='Last trip photo')
    last_trip_fleet_check_photo_datas = fields.Binary('Last trip photo datas', compute='_compute_last_trip_fleet_check_photo_datas')
    last_trip_fleet_check_photo_url = fields.Char('Last trip photo url', compute='_compute_last_trip_fleet_check_photo_url')

    
    # Campi relativi alle foto MASTER (Quelle che saranno controllate dall'AI)
    fleet_check_photo_master_id = fields.Many2one('ir.attachment', string="Foto master")
    fleet_check_photo_master_datas = fields.Binary(string="Foto master Datas", compute='_compute_fleet_check_photo_master_datas')
    fleet_check_photo_master_url = fields.Char(string="Foto master Url", compute='_compute_fleet_check_photo_master_url')
    fleet_check_photo_master_state = fields.Many2many('')
    fleet_check_photo_master_cam_id = fields.Many2one('fleet.check.cam')
    # Campi relativi alle immagini del mezzo di eventuali danni di categoria ancora in stato aperto
    last_trip_fleet_check_photo_master_id = fields.Many2one('ir.attachment', string='Last trip photo master')
    last_trip_fleet_check_photo_master_datas = fields.Binary('Last trip photo master datas', compute='_compute_last_trip_fleet_check_photo_master_datas')
    last_trip_fleet_check_photo_master_url = fields.Char('Last trip photo master url', compute='_compute_last_trip_fleet_check_photo_master_url')

    # fleet_check_photo_2_id = fields.Many2one('ir.attachment', string="Foto 2")
    # fleet_check_photo_2_datas = fields.Binary(string="Foto 2 Datas", compute='_compute_fleet_check_photo_2_datas')
    # fleet_check_photo_2_state = fields.Many2one()
    # fleet_check_photo_2_cam = fields.Char()
    
    # fleet_check_photo_3_id = fields.Many2one('ir.attachment', string="Foto 3")
    # fleet_check_photo_3_datas = fields.Binary(string="Foto 3 Datas", compute='_compute_fleet_check_photo_3_datas')
    # fleet_check_photo_3_state = fields.Many2one()
    # fleet_check_photo_3_cam = fields.Char()
    
    # fleet_check_photo_4_id = fields.Many2one('ir.attachment', string="Foto 4")
    # fleet_check_photo_4_datas = fields.Binary(string="Foto 4 Datas", compute='_compute_fleet_check_photo_4_datas')
    # fleet_check_photo_4_state = fields.Many2one()
    # fleet_check_photo_4_cam = fields.Char()
    
    # fleet_check_photo_5_id = fields.Many2one('ir.attachment', string="Foto 5")
    # fleet_check_photo_5_datas = fields.Binary(string="Foto 5 Datas", compute='_compute_fleet_check_photo_5_datas')
    # fleet_check_photo_5_state = fields.Many2one()
    # fleet_check_photo_5_cam = fields.Char()

    # fleet_check_photo_6_id = fields.Many2one('ir.attachment', string="Foto 6")
    # fleet_check_photo_6_datas = fields.Binary(string="Foto 6 Datas", compute='_compute_fleet_check_photo_6_datas')
    # fleet_check_photo_6_state = fields.Many2one()
    # fleet_check_photo_6_cam = fields.Char()
    
    # fleet_check_photo_7_id = fields.Many2one('ir.attachment', string="Foto 7")
    # fleet_check_photo_7_datas = fields.Binary(string="Foto 7 Datas", compute='_compute_fleet_check_photo_7_datas')
    # fleet_check_photo_7_state = fields.Many2one()
    # fleet_check_photo_7_cam = fields.Char()
    
    # fleet_check_photo_8_id = fields.Many2one('ir.attachment', string="Foto 8")
    # fleet_check_photo_8_datas = fields.Binary(string="Foto 8 Datas", compute='_compute_fleet_check_photo_8_datas')
    # fleet_check_photo_8_state = fields.Many2one()
    # fleet_check_photo_8_cam = fields.Char()
    
    # Recupero datas della foto
    @api.depends('fleet_check_photo_id')
    def _compute_fleet_check_photo_datas(self):
        for record in self:
            record.fleet_check_photo_datas = record.fleet_check_photo_id.datas if record.fleet_check_photo_id else False
    
    # Recupero url della foto        
    @api.depends('fleet_check_photo_id')
    def _compute_fleet_check_photo_url(self):
        for record in self:
            record.fleet_check_photo_url = record.fleet_check_photo_id.url if record.fleet_check_photo_id else False

    # Recupero datas della foto master
    @api.depends('fleet_check_photo_master_id')
    def _compute_fleet_check_photo_master_datas(self):
        for record in self:
            record.fleet_check_photo_master_datas = record.fleet_check_photo_master_id.datas if record.fleet_check_photo_master_id else False
    
    # Recupero url della foto master   
    @api.depends('fleet_check_photo_master_id')
    def _compute_fleet_check_photo_master_url(self):
        for record in self:
            record.fleet_check_photo_master_url = record.fleet_check_photo_master_id.url if record.fleet_check_photo_master_id else False
    
    
    ########### ORIGINAL
    # Recupero datas della foto
    @api.depends('last_trip_fleet_check_photo_id')
    def _compute_last_trip_fleet_check_photo_datas(self):
        for record in self:
            record.last_trip_fleet_check_photo_datas = record.last_trip_fleet_check_photo_master_id.datas if record.last_trip_fleet_check_photo_master_id else False
    # Recupero url della foto  
    @api.depends('last_trip_fleet_check_photo_id')
    def _compute_last_trip_fleet_check_photo_url(self):
        for record in self:
            record.last_trip_fleet_check_photo_url = record.last_trip_fleet_check_photo_id.url if record.last_trip_fleet_check_photo_id else False
    
    ########### MASTER
    # Recupero datas della foto master
    @api.depends('last_trip_fleet_check_photo_master_id')
    def _compute_last_trip_fleet_check_photo_master_datas(self):
        for record in self:
            record.last_trip_fleet_check_photo_master_datas = record.last_trip_fleet_check_photo_master_id.datas if record.last_trip_fleet_check_photo_master_id else False
    # Recupero url della foto master   
    @api.depends('last_trip_fleet_check_photo_master_id')
    def _compute_last_trip_fleet_check_photo_master_url(self):
        for record in self:
            record.last_trip_fleet_check_photo_master_url = record.last_trip_fleet_check_photo_master_id.url if record.last_trip_fleet_check_photo_master_id else False

#     @api.depends('fleet_check_photo_2_id')
#     def _compute_fleet_check_photo_2_datas(self):
#         for record in self:
#             record.fleet_check_photo_2_datas = record.fleet_check_photo_2_id.datas if record.fleet_check_photo_2_id else False
    
#     @api.depends('fleet_check_photo_3_id')
#     def _compute_fleet_check_photo_3_datas(self):
#         for record in self:
#             record.fleet_check_photo_3_datas = record.fleet_check_photo_3_id.datas if record.fleet_check_photo_3_id else False
    
#     @api.depends('fleet_check_photo_4_id')
#     def _compute_fleet_check_photo_4_datas(self):
#         for record in self:
#             record.fleet_check_photo_4_datas = record.fleet_check_photo_4_id.datas if record.fleet_check_photo_4_id else False
    
#     @api.depends('fleet_check_photo_5_id')
#     def _compute_fleet_check_photo_5_datas(self):
#         for record in self:
#             record.fleet_check_photo_5_datas = record.fleet_check_photo_5_id.datas if record.fleet_check_photo_5_id else False
    
#     @api.depends('fleet_check_photo_6_id')
#     def _compute_fleet_check_photo_6_datas(self):
#         for record in self:
#             record.fleet_check_photo_6_datas = record.fleet_check_photo_6_id.datas if record.fleet_check_photo_6_id else False
    
#     @api.depends('fleet_check_photo_7_id')
#     def _compute_fleet_check_photo_7_datas(self):
#         for record in self:
#             record.fleet_check_photo_7_datas = record.fleet_check_photo_7_id.datas if record.fleet_check_photo_7_id else False
    
#     @api.depends('fleet_check_photo_8_id')
#     def _compute_fleet_check_photo_8_datas(self):
#         for record in self:
#             record.fleet_check_photo_8_datas = record.fleet_check_photo_8_id.datas if record.fleet_check_photo_8_id else False

#     def ciao_1(self):
#         _logger.info("CIAO")
        
#     def ciao_2(self):
#         _logger.info("CIAO")
    
# # class VehicleCheckPhoto(models.Model):
# #     _name = "fleet.check.photo"
# #     _description = "Fleet check photo"
    
    
# #     name = fields.Char()
# #     attachment_id = fields.Many2one('ir.attachment')
    
