{
    'name': 'Fleet check',
    'version': '16',
    'author': "Luca Cocozza",
    'application': True,
    'description': "This module is used to manage the photos taken of the vehicles by the facility.",
    'depends': [
        'survey',],
    'data': [
        # # # Settaggi per accesso ai contenuti
        'data/ir.model.access.csv',
        # # # Caricamento delle view,
        'view/fleet_check.xml',
        # # Menu
        'view/menu.xml',
    ],
}
