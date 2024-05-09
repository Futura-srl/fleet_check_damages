{
    'name': 'Fleet check',
    'version': '16',
    'author': "Luca Cocozza",
    'application': True,
    'description': "This module is used to manage the photos taken of the vehicles by the facility.",
    'depends': [
        'survey',
        'gtms',
        'fleet_service_with_deduction',
        'hr',
        'fleet',
        'automatic_fleet_management',
        'hr',
        ],
    'data': [
        # # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # # Caricamento delle view,
        'view/fleet_check.xml',
        'view/fleet_check_cam.xml',
        'view/fleet_check_import_log.xml',
        # # Menu
        'view/menu.xml',
    ],
}
