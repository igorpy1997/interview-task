# -*- coding: utf-8 -*-
{
    'name': 'Interview Task',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom module for interview task - extends sale orders',
    'description': """
        Interview Task Module
        ======================
        This module extends sale order functionality:
        - Adds width and height fields to sale order lines
        - Calculates square meters automatically
        - Manages delivery term types and dates
    """,
    'author': 'Interview Candidate',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/delivery_term_type_views.xml',
        'data/delivery_term_type_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
