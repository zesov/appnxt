# -*- coding: utf-8 -*-
{
    'name': "nxt_restful_api",

    'summary': """
        This module provide RESTful API (json) access to Odoo models.
        """,

    'description': """
        This module provide RESTful API (json) access to Odoo models.
    """,

    'author': "63720750@qq.com",
    'website': "http://www.appnxt.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
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
}