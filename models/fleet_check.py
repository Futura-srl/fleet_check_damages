from odoo import fields, models, api
import logging
from datetime import datetime, timedelta
import os, csv, base64


_logger = logging.getLogger(__name__)



class VehicleCheck(models.Model):
    _name = "fleet.check"
    _description = "Fleet check"
    _inherit = "mail.thread"

    name = fields.Char()
    state = fields.Selection([('new','New'),('damages','With Damages'),('done','No Damages'),('old','Older')], default='new', compute='_update_state_fleet_check', store=True)
    damage_ids= fields.Many2many('fleet.damage.type', 'name')
    trip_id = fields.Many2one('gtms.trip', string="Trip")
    datetime_trip_id = fields.Datetime(compute='_compute_datetime_trip_id', store=True)
    vehicle_id = fields.Many2one('fleet.vehicle', compute='_compute_vehicle_id', store=True)
    older_damages = fields.Boolean()
    no_damages = fields.Boolean()
    trip_processed = fields.Boolean()

    # dati viaggio precedente
    damages_open_ids = fields.One2many('reparation.reparation', compute='_compute_damages_open', string='Damages open')
    last_trip_id = fields.Many2one('gtms.trip', compute='_compute_last_trip_id')


    # Toggle per visualizzazioni
    original_bool = fields.Boolean(string="Original")
    master_bool = fields.Boolean(string="Master")
    all_bool = fields.Boolean(string="All")

    # Campi relativi alle foto originali e non modificate dall'AI
    fleet_check_photo_id = fields.Many2one('ir.attachment', string="Foto")
    fleet_check_photo_datas = fields.Binary(string="Foto Datas", compute='_compute_fleet_check_photo_datas')
    fleet_check_photo_url = fields.Char(string="Foto Url", compute='_compute_fleet_check_photo_url')
    fleet_check_photo_state = fields.Many2one('')
    fleet_check_photo_cam_id = fields.Many2one('fleet.check.cam')
    # Campi relativi alle immagini del mezzo di eventuali danni di categoria ancora in stato aperto
    last_trip_fleet_check_photo_id = fields.Many2one('ir.attachment', string='Last trip photo', compute="_compute_last_trip_fleet_check_photo_id")
    last_trip_fleet_check_photo_datas = fields.Binary('Last trip photo datas', compute='_compute_last_trip_fleet_check_photo_datas')
    last_trip_fleet_check_photo_url = fields.Char('Last trip photo url', compute='_compute_last_trip_fleet_check_photo_url')

    
    # Campi relativi alle foto MASTER (Quelle che saranno controllate dall'AI)
    fleet_check_photo_master_id = fields.Many2one('ir.attachment', string="Foto master")
    fleet_check_photo_master_datas = fields.Binary(string="Foto master Datas", compute='_compute_fleet_check_photo_master_datas')
    fleet_check_photo_master_url = fields.Char(string="Foto master Url", compute='_compute_fleet_check_photo_master_url')
    fleet_check_photo_master_state = fields.Many2many('')
    fleet_check_photo_master_cam_id = fields.Many2one('fleet.check.cam')
    # Campi relativi alle immagini del mezzo di eventuali danni di categoria ancora in stato aperto
    last_trip_fleet_check_photo_master_id = fields.Many2one('ir.attachment', string='Last trip photo master', compute="_compute_last_trip_fleet_check_photo_master_id")
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


    # # funzione per sapere (lato server) quali record sono ancora da gestire, per convenzione saranno mostrati tutti i record in ordine di data viaggio e stato =
    # def record_to_check(self):
    #     records = self.env['fleet.check'].search_read([('state', '=', 'new')], ['trip_id'])
    #     _logger.info(records)
    #     all_records = []
    #     for record in records:
    #         all_records.append(record['trip_id'][0])

    #     _logger.info("Lista di tutti i record ancora da controllare in ordine di data viaggio")
    #     _logger.info(all_records)
    #     records = self.env['gtms.trip'].search([('id', 'in', all_records)], order="first_stop_planned_at asc")
    #     _logger.info(records)
    #     break
    #     return records


    # Recupero il datetime del viaggio associato
    @api.depends('trip_id')
    def _compute_datetime_trip_id(self):
        for record in self:
            test = self.env['gtms.trip'].search_read([('id', '=', record.trip_id.id)], ['first_stop_planned_at'])
            record.datetime_trip_id = test[0]['first_stop_planned_at']
            # _logger.info('first_stop_planned_at')
            # _logger.info(test[0]['first_stop_planned_at'])

    
    # Recupero datas della foto original
    @api.depends('fleet_check_photo_id')
    def _compute_fleet_check_photo_datas(self):
        for record in self:
            record.fleet_check_photo_datas = record.fleet_check_photo_id.datas if record.fleet_check_photo_id else False
    
    # Recupero url della foto original        
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
    # Recupero datas della foto original del viaggio precedente
    @api.depends('last_trip_fleet_check_photo_id')
    def _compute_last_trip_fleet_check_photo_datas(self):
        # _logger.info("Provo 4")
        for record in self:
            record.last_trip_fleet_check_photo_datas = record.last_trip_fleet_check_photo_id.datas if record.last_trip_fleet_check_photo_id else False
    
    # Recupero url della foto original del viaggio precedente 
    @api.depends('last_trip_fleet_check_photo_id')
    def _compute_last_trip_fleet_check_photo_url(self):
        # _logger.info("Provo 3")
        for record in self:
            record.last_trip_fleet_check_photo_url = record.last_trip_fleet_check_photo_id.url if record.last_trip_fleet_check_photo_id else False
    
    ########### MASTER
    # Recupero datas della foto master del viaggio precedente
    @api.depends('last_trip_fleet_check_photo_master_id')
    def _compute_last_trip_fleet_check_photo_master_datas(self):
        # _logger.info("Provo 2")
        for record in self:
            record.last_trip_fleet_check_photo_master_datas = record.last_trip_fleet_check_photo_master_id.datas if record.last_trip_fleet_check_photo_master_id else False
    
    # Recupero url della foto master del viaggio precedente   
    @api.depends('last_trip_fleet_check_photo_master_id')
    def _compute_last_trip_fleet_check_photo_master_url(self):
        # _logger.info("Provo 1")
        
        for record in self:
            record.last_trip_fleet_check_photo_master_url = record.last_trip_fleet_check_photo_master_id.url if record.last_trip_fleet_check_photo_master_id else False

    ################# Recupero targa dal viaggio
    @api.depends('trip_id')
    def _compute_vehicle_id(self):
        for record in self:
            # _logger.info("_compute_vehicle_id")
            # _logger.info(f"{record.trip_id.current_fleet_id.id}")
            record.vehicle_id = record.trip_id.current_fleet_id.id
            # _logger.info(f"STAMPO LA TARGA = {self.trip_id.current_fleet_id}")
            # self.vehicle_id = self.trip_id.current_fleet_id
            # _logger.info(f"STAMPO self.vehicle_id = {self.vehicle_id}")

    ################# Funzione per recuperare il viaggio precedente
    @api.depends('trip_id')
    def _compute_last_trip_id(self):
        for record in self:
            # _logger.info("_compute_last_trip_id")
            record.last_trip_id = self.env['gtms.trip'].search([('current_fleet_id', '=', record.trip_id.current_fleet_id.id), ('first_stop_planned_at', '<', record.trip_id.first_stop_planned_at)], limit=1, order="id desc")
            # _logger.info(f" STAMPO IL VIAGGIO ESEGUITO PRECEDENTEMENTE CON QUESTO MEZZO = {record.last_trip_id.id}")
    
    ################# Funzione per recuperare le foto original del viaggio precedente
    @api.depends('last_trip_id', 'fleet_check_photo_cam_id')
    def _compute_last_trip_fleet_check_photo_id(self):
        for record in self:
            # _logger.info(f"VIAGGIO PRECEDENTE = {record.last_trip_id.id}")
            record.last_trip_fleet_check_photo_id = self.env['fleet.check'].search([('trip_id', '=', record.last_trip_id.id),('fleet_check_photo_cam_id', '=', record.fleet_check_photo_cam_id.id)]).fleet_check_photo_id
            # Cerco il record id foto associato al viaggio precedente
            # _logger.info("_compute_last_trip_fleet_check_photo_id")
            test = self.env['fleet.check'].search([('trip_id', '=', record.last_trip_id.id),('fleet_check_photo_cam_id', '=', record.fleet_check_photo_cam_id.id)])
            # _logger.info("Test foto viaggio precedente! original")
            # _logger.info(test.fleet_check_photo_cam_id)
            # _logger.info(record.last_trip_fleet_check_photo_id)
            # _logger.info(record.last_trip_fleet_check_photo_id.datas)
            # _logger.info(record.last_trip_fleet_check_photo_id.url)
            
    ################# Funzione per recuperare le foto master del viaggio precedente
    @api.depends('last_trip_id', 'fleet_check_photo_cam_id')
    def _compute_last_trip_fleet_check_photo_master_id(self):
        for record in self:
            test = self.env['fleet.check'].search([('trip_id', '=', record.last_trip_id.id)])
            record.last_trip_fleet_check_photo_master_id = self.env['fleet.check'].search([('trip_id', '=', record.last_trip_id.id),('fleet_check_photo_cam_id', '=', record.fleet_check_photo_cam_id.id)]).fleet_check_photo_master_id
            # Cerco il record id foto associato al viaggio precedente
            # _logger.info("_compute_last_trip_fleet_check_photo_master_id")
            # _logger.info("Test foto viaggio precedente!")
            # _logger.info(test.fleet_check_photo_cam_id)
            
    
    ################# 
    @api.depends('trip_id')
    def _compute_damages_open(self):
        for record in self:
            # _logger.info("_compute_damages_open")
            test = self.env['reparation.reparation'].search([('fleet_id', '=', record.vehicle_id.id), ('state', '=', 'open'), ('fleet_vehicle_log_service_id.date', '<=', record.trip_id.first_stop_planned_at)], order="event_date desc")
            record.damages_open_ids = [reparation.id for reparation in test]  # Estrai gli ID dalla lista di record
            if record.damages_open_ids == []:
                record.damages_open_ids = None
            # _logger.info(record.damages_open_ids)


    @api.depends('damage_ids', 'older_damages', 'no_damages')
    def _update_state_fleet_check(self):
        for record in self:
            # _logger.info(f"STAMPO damage_ids = {record.damage_ids}")
            if record.damage_ids:
                # _logger.info(f"Ci sono danni")
                record.state = 'damages'
            elif record.older_damages == True:
                # _logger.info(f"Sono danni vecchi")
                record.state = 'old'
            elif record.no_damages == True:
                # _logger.info(f"Non ci sono danni")
                record.state = 'done'
            else:
                # _logger.info(f"Da controllare")
                record.state = 'new'
                
            
    def fleet_check_set_older(self):
        _logger.info("ADESSO GENERO revious_search_ids E LO STAMPO!!!")
        revious_search_ids = self.env.context.get('previous_search_ids', [])
        _logger.info(revious_search_ids)
        for record in self:
            _logger.info(f"Sono danni vecchi")
            record.older_damages = True
            next_record = self.env['fleet.check'].search([('state', '=', 'new')], order="datetime_trip_id asc", limit=1)
            _logger.info(next_record)
            if next_record:
                return {
                'type': 'ir.actions.act_window',
                'name': 'Fleet Check',
                'view_mode': 'form',
                'res_model': 'fleet.check',
                'res_id': next_record[0].id
            }

    def fleet_check_set_no_damages(self):
        for record in self:
            _logger.info(f"Non ci sono danni")
            record.no_damages = True
            next_record = self.env['fleet.check'].search([('state', '=', 'new')], order="datetime_trip_id asc", limit=1)
            _logger.info(next_record)
            if next_record:
                return {
                'type': 'ir.actions.act_window',
                'name': 'Fleet Check',
                'view_mode': 'form',
                'res_model': 'fleet.check',
                'res_id': next_record[0].id
            }
            
    def fleet_check_reset(self):
        for record in self:
            record.older_damages = False
            record.no_damages = False


    # Creo la funzione che cicla tutti i record e mi estrae i viaggi ed elimino i doppioni
    # Per ogni viaggio controllo se ci sono cam con ancora lo stato in 'new'
    # Se ci sono salto il numero di viaggio
    # Se tutti gli stati sono 'done' o 'older' metto True a trip_processed
    # Se tutti gli stati sono != 'new' e almeno uno è = 'damages' per ogni cam vedo i danni rilevati e creo un'anomalia con quei dati (tipologia danno, data evento)


    
    def check_all_cams(self):
        _logger.info(self)
        
        trips_not_processed = []
        _logger.info(self)
        for record in self:
            _logger.info(f"record.trip_processed {record.trip_processed}")
            _logger.info(f"record.trip_processed {record}")
            if record.trip_processed == True:
                continue
            else:
               trips_not_processed.append(record.id) 
        # trips_not_processed = self.env['fleet.check'].search_read([('trip_processed', '=', False)], ['trip_id'])
        unique_values = trips_not_processed
        unique_values = list(unique_values)
        _logger.info(f'STAMPO trips_not_processed\n{trips_not_processed}')
        _logger.info(f'STAMPO unique_values\n{unique_values}')
        trips = []
        for trip in trips_not_processed:
            trips.append(trip)
        trips_not_processed_unique = list(set(trips))
        # trips = []
        trips_with_new_damages = []
        trips_with_no_new_damages = []
        _logger.info(trips_not_processed_unique)
        
        # Per ogni viaggio controllo se ci sono cam con ancora lo stato in 'new'
        for trip_not_processed in trips_not_processed_unique:
            is_trip_not_processable = self.env['fleet.check'].search([('id', '=', trip_not_processed), ('state', '=', 'new')])
            _logger.info(f'is_trip_not_processable = {is_trip_not_processable.trip_id}')
            cams_not_new = self.env['fleet.check'].search([('id', '=', trip_not_processed)])
            _logger.info(f'cams_not_new = {cams_not_new}')
            _logger.info
            if not is_trip_not_processable:
                for cam_not_new in cams_not_new:
                    trips.append(trip_not_processed)
        _logger.info("STAMPO VIAGGI CON CAMS state != 'new' and trip_processed == False")
        trips = list(set(trips))
        _logger.info(trips)


        is_trips_with_damages = []
        # Per ogni viaggio controllo se ci sono cam con lo stato 'damages'
        for trip_not_processed in trips:
            _logger.info(f'STAMPO trip_not_processed {trip_not_processed}')
            is_trips_with_damages.append(self.env['fleet.check'].search([('id', '=', trip_not_processed), ('state', '=', 'damages')]))
            _logger.info(f'is_trips_with_damages = {is_trips_with_damages}')
            if not is_trips_with_damages:
                self.env['fleet.check'].search([('id', '=', trip_not_processed)],['trip_id'])
                # trips_with_no_new_damages.append(trip_not_processed['trip_id'])
                trips_with_no_new_damages.append(self.env['fleet.check'].search([('id', '=', trip_not_processed)]))
            else:
                for is_trip_with_damages in is_trips_with_damages:
                    _logger.info(f'is_trip_with_damages = {is_trip_with_damages.trip_id}')
                    _logger.info(self.env['fleet.check'].search([('id', '=', trip_not_processed)])[0].trip_id)
                    if is_trip_with_damages:
                        _logger.info(f"STAMPO trip {self.env['fleet.check'].search([('id', '=', trip_not_processed)])}")
                        _logger.info(f"STAMPO is_trip_with_damages {is_trip_with_damages.trip_id.id}")
                        trip_id = self.env['fleet.check'].search([('id', '=', is_trip_with_damages.id)])
                        _logger.info(trip_id.trip_id.id)
                        if trip_id.trip_id.id == is_trip_with_damages.trip_id.id:
                            trips_with_new_damages.append(self.env['fleet.check'].search([('id', '=', trip_not_processed)]))
                            _logger.info(f"Ho aggiunto un danno : {self.env['fleet.check'].search([('id', '=', trip_not_processed)])}")

        trips_with_new_damages = set(trips_with_new_damages)
        trips_id = []
        for t_id in trips_with_new_damages:
            trips_id.append(t_id.trip_id)
        trips_with_no_new_damages = set(trips_with_no_new_damages)        
        _logger.info(f'STAMPO VIAGGI CON DANNO {trips_with_new_damages}')
        _logger.info(f'STAMPO VIAGGI SENZA DANNO {trips_with_no_new_damages}')
        for danno in trips_id:
            _logger.info(f"Creo un'anomalia per questo viaggio -> {danno.id}")
            cams = self.env['fleet.check'].search([('trip_id', '=', danno.id)])
            self.add_new_deduction(danno)
            for cam in cams:
                # Inserire funzione che crea anomalia e che metta la cam del viaggio come processata
                cam.trip_processed = False
                
        for no_danno in trips_with_no_new_damages:
            _logger.info(f"Per questo viaggio imposto trip_processed = True -> {no_danno}")
            cams = self.env['fleet.check'].search([('trip_id', '=', no_danno)])
            for cam in cams:
                # Inserire funzione che metta la cam del viaggio come processata
                cam.trip_processed = True


    # Funzione per creare un'anomalia
    def add_new_deduction(self, danno):
        _logger.info(f"STAMPO DANNO {danno.id}")
        cams = self.env['fleet.check'].search([('trip_id', '=', danno.id)])
        trip = self.env['gtms.trip'].search([('id', '=', danno.trip_id.id)])
        data = {}
        reparation = list([])
        documents = list([])
        for cam in cams:
            _logger.info('start add_new_deduction')
            _logger.info(trip[0])
            _logger.info(trip[0].first_stop_planned_at.strftime("%Y-%m-%d"))
            if cam.damage_ids.id == False:
                continue
            else:
                reparation.append((0, 0, {'damage_type_id': cam.damage_ids.id, 'state': 'open', 'date': trip[0].first_stop_planned_at.strftime("%Y-%m-%d") }))
                if cam.fleet_check_photo_id.url:
                    _logger.info(self.env['documents.document'].search([('attachment_id', '=', cam.fleet_check_photo_id.id)]))
                    documents.append((0, 0, {'attachment_id': cam.fleet_check_photo_id.id, 'tag_ids': [59], 'name': cam.fleet_check_photo_id.name, 'folder_id': 4, 'type': 'url' }))
                else:
                    documents.append((0, 0, {'attachment_id': cam.fleet_check_photo_id.id, 'tag_ids': [59], 'name': cam.fleet_check_photo_id.name, 'folder_id': 4, 'type': 'binary' }))
        _logger.info(reparation)
        _logger.info(documents)
        current_date = datetime.now()
        data = {
            'description': "Anomalia ",
            'service_type_id': 9,
            'date': danno.trip_id.first_stop_planned_at.strftime("%Y-%m-%d %H:%M:%S"), # data evento
            'amount': 0.0,
            'trip_id': danno.trip_id.id,
            'vehicle_id': danno.trip_id.current_fleet_id.id,
            'purchaser_id': danno.trip_id.current_driver_id.id,
            'company_id': danno.trip_id.company_ids[0].id,
            'responsibility': False,
            'repair_mode': False,
            'start_date': current_date, # Orario creazione anomalia
            'reparation_ids': reparation, # Tipologia di danno, stato aperto e data evento
            'document_ids': documents # Tipologia di danno, stato aperto e data evento
        }
        _logger.info(data)
        create_service = self.env['fleet.vehicle.log.services'].create(data)
        _logger.info(f"HO CREATO ANOMALIA CON ID = {create_service}")
        self.create_reminder(create_service)


    def import_photo_check(self):
        current_directory = os.getcwd()

        _logger.info(f"The current working directory is: {current_directory}")
        _logger.info("PARTO ALLA RICERCA DEL CSV")
        # Percorso della directory da scansionare
        directory = "./photo-check/"
        _logger.info(os.walk(directory))
        # Scansione ricorsiva della directory e delle sottodirectory
        for root, dirs, files in os.walk(directory):
            _logger.info("Scansione della directory: %s", root)
            for file in files:
                # Verifica se il file è un file CSV
                if file.endswith(".csv"):
                    # Ottieni il percorso completo del file CSV
                    file_csv = os.path.join(root, file)
                    _logger.info("File CSV trovato: %s", file_csv)
                    # Leggi e stampa i valori delle colonne del file CSV
                    self.leggi_e_stamp_csv(file_csv, file)

        

    def leggi_e_stamp_csv(self, file_csv, file):
        _logger.info("Lettura del file CSV: %s", file_csv)
        
        # Leggi il contenuto del file CSV
        with open(file_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            # Controllo se il file esiste già tra gli allegati di Odoo; in alternativa, lo processo e lo carico
            csv_id = self.env['ir.attachment'].search([('name', '=', file)])
            if csv_id:
                _logger.info("Il file CSV risulta già importato")
                return
            else:
                _logger.info("Il file CSV verrà importato")
                
                # Leggi il contenuto del file e convertilo in bytes
                csvfile.seek(0)  # Torna all'inizio del file per leggerlo nuovamente
                content = csvfile.read()
                content_bytes = content.encode('utf-8')
                
                # Codifica in base64 il contenuto in bytes
                file_base64 = base64.b64encode(content_bytes).decode('utf-8')
                _logger.info("Base64 del file: %s", file_base64)

                # Faccio l'upload nella tabella ir.attachment di odoo del file csv
                data = {
                    'name': file, 
                    'type': 'binary', 
                    'datas': file_base64, 
                }
                file_id = self.env['ir.attachment'].create(data)
                _logger.info(f"STAMPO ID RECORD CREATO {file_id.id}")
                
                # Torna all'inizio del file dopo la lettura per processare le righe
                csvfile.seek(0)
                
                for riga in reader:
                    if len(riga) >= 4:
                        camera = riga[0]
                        datetime_csv = datetime.strptime(riga[1], '%Y%m%d%H%M%S')
                        date_trip = datetime.strptime(riga[1], '%Y%m%d%H%M%S').date()
                        start_of_day = date_trip
                        end_of_day = date_trip + timedelta(days=1)
                        esito = riga[2] == "True"
                        photo_name = riga[3]
                        errore = riga[4]

                        fleet_id = None
                        filename = file
                        # Divide la stringa sul simbolo '_'
                        parts = filename.split('_')
                        # Prende la seconda parte e rimuove l'estensione '.csv'
                        license_plate = parts[1].replace('.csv', '')

                        fleet = self.env['fleet.vehicle'].search([('license_plate', '=', license_plate)])
                        if fleet != []:
                            fleet_id = fleet.id

                            # Recupero il viaggio associato al mezzo e con data inizio 
                            # Cerco tutti i viaggi eseguiti con il mezzo specifico nella data specifica
                            # Il viaggio che poi mi interessa è trip_start_from_survey <= datetime_csv, trip_start_from_survey >= datetime_csv oppure trip_start_from_survey <= datetime_csv, trip_start_from_survey == False
                            trips = self.env['gtms.trip'].search([('current_fleet_id', '=', fleet_id), ('trip_start_from_survey', '>=', start_of_day), ('trip_start_from_survey', '<', end_of_day)])
                            trip_id = self.env['gtms.trip'].search([('id', 'in', trips.ids), ('trip_start_from_survey', '<=', datetime_csv), ('trip_end_from_survey', '>=', datetime_csv)])
                            _logger.info(trips)
                            _logger.info(trip_id)
                            if len(trip_id) != 1:
                                trip_id = None
                            # '|', ('trip_start_from_survey', '<=', datetime_csv), ('trip_start_from_survey', '=', False)
                        _logger.info("Photo name: %s", photo_name)
                        _logger.info("Targa: %s, fleet_id %s", license_plate, fleet_id)
                        _logger.info("Camera: %s", camera)
                        _logger.info("Datetime_csv: %s", datetime_csv)
                        _logger.info("Esito: %s", esito)
                        _logger.info("Errore: %s", errore)
                        
                        cam = self.env['fleet.check.cam'].search_read([('cam_code', '=', camera)])
                        cam_id = None
                        # _logger.info(cam[0]['id'])

                        if cam != []:
                            cam_id = cam[0]['id']

                        data = {
                            'name': file,
                            'cam_code': cam_id,
                            'datetime_photo': str(datetime_csv),
                            'photo_name': photo_name,
                            'esito': esito,
                            'cam_error': errore,
                            'attachment_csv_id': file_id.id,
                            'fleet_id': fleet_id,
                            'trip_id': trip_id.id,
                        }
                        log = self.env['fleet.check.import.log'].create(data)
                        _logger.info(log)

        # Dopo aver gestito il file viene eliminato
        os.remove(file_csv)
        _logger.info("File CSV eliminato: %s", file_csv) 


    # Funzione per importare le foto nel db e l'eliminazione del file fisico dalla cartella
    # Controllo nella tabella fleet.check.import.log se ci sono record con export_processed == False, esito == True, export_processed == False e state == 'new'
    # I record trovati saranno quelli da importare nel db
    # L'importazione avverrà in automatico con la creazione del fleet.check (ovvero un record per foto)
    def import_photo_to_fleet_check(self):
        all_records = self.env['fleet.check.import.log'].search([('export_processed', '=', False), ('esito', '=', True), ('state', '=', 'new')], order="trip_id asc")
        for record in all_records:
            # Carico la foto in attachment e poi la associo al fleet_check
            foto_id = self.get_base64_photo_and_upload(record.photo_name)
            data = {
                'vehicle_id': record.fleet_id.id,
                'trip_id': record.trip_id.id,
                'original_bool': True,
                'fleet_check_photo_id': foto_id,
                'name': 'test',
            }
            check = self.env['fleet.check'].create(data)
            record.export_processed = True

    # Funzione per ottenere il base64 di una foto e caricarla in ir.attachment
    def get_base64_photo_and_upload(self, photo_name):
        current_directory = os.getcwd()
        _logger.info(f"The current working directory is: {current_directory}")
        _logger.info("PARTO ALLA RICERCA DELLA FOTO")
    
        # Percorso della directory da scansionare
        directory = "./photo-check/"
    
        # Percorso completo del file
        file_path = os.path.join(directory, photo_name)
    
        # Verifica se il file esiste
        if os.path.isfile(file_path):
            _logger.info("File trovato: %s", file_path)
    
            # Legge il contenuto del file
            with open(file_path, "rb") as file:
                file_content = file.read()
    
            # Codifica in base64 il contenuto in bytes
            file_base64 = base64.b64encode(file_content).decode('utf-8')
    
            _logger.info("Base64 del file: %s", file_base64)
    
            # Faccio l'upload nella tabella ir.attachment di odoo del file csv
            data = {
                'name': photo_name, 
                'type': 'binary', 
                'datas': file_base64, 
            }
            file_id = self.env['ir.attachment'].create(data)
    
            _logger.info("File caricato con ID: %s", file_id.id)
            os.remove(file_path)
            return file_id.id
        else:
            _logger.error("File non trovato: %s", file_path)
            return None
        
    
    def log_files_in_directory(self):
        directory = "./photo-check/"
        _logger.info(f"Scansione della cartella: {directory}")
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                _logger.info(f"File trovato: {filepath}")
        
    def test_fleet_check(self):
        _logger.info(f"TEST DELLA FUNZIONE FLEET CHECK")
        _logger.info(self)
        for record in self:
            _logger.info(record)
        self.import_photo_check()
        
    def create_reminder(self, res):
        _logger.info(f"Stampo il fottuto self {res.id}")
        # Il cdc va pescato dal viaggio associato o (come seconda opzione) dal contratto di disponibilità
        # Verifico se ci sono viaggi associati
        if res[0]['trip_id'] != False: 
            # Recupero il cdc associato al viaggio
            _logger.info("CERCO L'ID CDC")
            cdc_id = self.env['gtms.trip'].search_read([('id', '=', res[0]['trip_id'].id)], ['organization_id'])
        else:
            # recupero il cdc dall'ultimo contratto di disponibilità
            cdc_id = self.env['fleet.vehicle.log.contract'].search_read([('vehicle_id', '=', res[0]['vehicle_id']), ('cost_subtype_id', '=', 47)], order='id desc',limit=1)
        helpdesk_id = self.env['helpdesk.team'].search_read([('organization_id', '=', cdc_id[0]['organization_id'][0])])
    
        if not helpdesk_id:
            raise ValidationError(_("Errore nella creazione dell'anomalia e del reminder. Non sei un ROP autorizzato. Per farsi aggiungere contattare raffaele.tesolin@futurasl.com o il 0431/611714."))
        
        _logger.info(cdc_id[0]['organization_id'][0])
        _logger.info(helpdesk_id)
        service_type = res.env['fleet.vehicle.log.services'].search_read([('id', '=', res.id)])
        _logger.info(service_type[0]['service_type_id'][0])
        if service_type[0]['service_type_id'][0] == 9:
            _logger.info("DEVO CREARE UN REMINDER")
            for user in helpdesk_id[0]['message_partner_ids']:
                user_id = self.env['res.users'].search_read([('partner_id', '=', user)], ['id'])
                _logger.info(user_id[0]['id'])
                alert = self.env['mail.activity'].create({
                    'res_name': 'Completamento sinistro ' + str(res['id']),
                    'activity_type_id': 26,
                    'user_id': user_id[0]['id'],
                    'res_model_id': 383, # id di fleet.vehicle.log.service
                    'res_id': res['id'],
                    'note': "<p style='margin-bottom:0px'>Per procedere allo step 'Segnalato' il sinistro deve essere completato con le seguenti informazioni:</p><ul style='margin-bottom:0px'><li>Modulo dichiarazione danno</li><li>Note descrittive</li></ul><li>Eventuale CID</li><li>Eventuali foto</li>"
                })
                _logger.info(alert)
