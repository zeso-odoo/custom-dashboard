{
    'name': 'Custom Dashboard',
    'version': '17.0.1.0.0',
    'summary': 'Share dashboard with teams',
    'category':'Dashboard',
    'description': """
        Custom Dashboard
    """,
    'author': 'Odoo Ps',
    'website': "https://www.odoo.com",
    'depends':[
        'board',
        'spreadsheet_dashboard',
    ],
    'data': [
        'views/ir_ui_view_views.xml',
        'views/dashboard_menu.xml',
    ],
    'assets':{
        'web.assets_backend': [
            'custom_dashboard/static/src/**/*.js',
            'custom_dashboard/static/src/**/*.xml',
        ],
    },
    'installable': True,
    'application':True,
    'license': 'LGPL-3',
}
