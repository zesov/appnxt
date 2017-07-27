# -*- coding: utf-8 -*-
{
    'name': "NXT restful api",

    'summary': """
        This module provide RESTful API (json) access to Odoo models.
        """,

    'description': """
        This module provide RESTful API (json) access to Odoo models.
        supported by Shanghai Panlu network technology. Ltd.
    """,

    'author': "appnxt.com",
    'website': "http://appnxt.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/appnxt.png'],
    "installable": True,
    "application": False,
    'live_test_url': 'http://d10c.y.appnxt.com/',
    # 'price': 9.99,
    # 'currency': 'EUR',
}