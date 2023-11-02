# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'gsi_elarning',
    'version' : '1.0',
    'summary': 'Gsi Elearning Platform',
    'sequence': 1,
    'description': """
    Gsi Elearning Platform
    """,
    'category': 'Web',
    'website': 'https://www.odoo.com/documentation/14.0/developer/howtos/rdtraining/03_newapp.html',
    'images' : [],
    'depends' : [
        'base',
        'sale',
        'sale_management',
        'website_slides',
        'website'
        ],
    'data': [
        'data/website_data.xml',
        # 'security/ir.model.access.csv',
        'views/auth_signup_login_templates.xml',
        # 'views/res_users_views.xml',
        'views/res_partner_view.xml',
        'views/assets.xml',
        'views/slide_channel_views.xml',
        'views/head_website_template.xml',
        'views/footer_website_template.xml',
        'views/navbar_menu_elearning_template.xml',
        'views/website_elearning_home_template.xml',
        'views/course_templates.xml',
        'views/training_workshop_website.xml',
        'views/event_elearning_template.xml',
        'views/blog_elearning_template.xml',
        'views/about_elearning_template.xml',
        'views/login_template.xml',
        'views/signup_template.xml',
        'views/user_profile_template.xml',
        
    ],
    'demo': [
        
    ],
    'qweb': [],
      
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
