# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Channel(models.Model):
    _inherit = 'slide.channel'

    # website_category = fields.Selection(string='Website Category', selection=[('popular', 'Popular')], default='popular')
    # code_test = fields.Char('Reference')
    popular = fields.Boolean(string='Popular')
    home_page = fields.Boolean(string='Home page')
    type_event = fields.Selection([('course', 'Course'), ('training_workshop', 'Training & Worskhop'),('event', 'Event')])
    date_course = fields.Date(string="Date")
    location = fields.Char(string="Location")
    description_home_page = fields.Char(string="Description home page")