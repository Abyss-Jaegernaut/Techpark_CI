{
    'name': 'IT Parc',
    'version': '18.0.1.0.0',
    'category': 'IT Management',
    'summary': 'Gestion centralisée du parc informatique de TECHPARK CI',
    'description': """
        Module personnalisé pour la gestion du parc informatique :
        - Inventaire des équipements
        - Historique des affectations
        - Suivi des maintenances
        - Gestion des contrats fournisseurs et alertes
        - Tableau de bord OWL interactif
    """,
    'author': 'TECHPARK CI',
    'website': 'https://www.techpark.ci',
    'depends': [
        'base', 
        'hr', 
        'stock', 
        'purchase', 
        'account', 
        'maintenance', 
        'mail', 
        'contacts', 
        'web'
    ],
    'data': [
        'security/parc_securite.xml',
        'security/ir.model.access.csv',
        'data/it_parc_data.xml',
        'wizards/reaffectation_wizard_views.xml',
        'wizards/renouvellement_contrat_wizard_views.xml',
        'wizards/scan_alertes_wizard_views.xml',
        'wizards/import_csv_wizard_views.xml',
        'views/equipement_views.xml',
        'views/affectation_views.xml',
        'views/intervention_views.xml',
        'views/contrat_views.xml',
        'views/alerte_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/it_parc_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # OWL components will go here later
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
