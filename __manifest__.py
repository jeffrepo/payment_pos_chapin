# -*- coding: utf-8 -*-

{
    'name': 'Pos chaping web',
    'category': 'Accounting/Payment',
    'summary': 'Pago en web: pos chaping implementacion',
    'version': '1.0',
    'description': """Pago POS CHAPIN""",
    'depends': ['base','payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_poschapin_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': [],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
