# -*- coding: utf-8 -*-
{
    'name': 'Interview',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Sales order extensions for interview task',
    'description': """
        Interview module that extends sale.order.line with:
        - Width and height fields
        - Square meters calculation
        - Delivery term types
        - Delivery date calculation
        - Automated delivery date updates via cron
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/delivery_term_type_views.xml',
        'data/delivery_term_type_data.xml',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}