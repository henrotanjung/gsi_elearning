
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from ast import literal_eval
from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.misc import ustr

from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.addons.auth_signup.models.res_partner import SignupError, now

_logger = logging.getLogger(__name__)


class ResUse(models.Model):
    _inherit = "res.users"

    
    state = fields.Selection(compute='_compute_state', search='_search_state', string='Status',
                 selection=[('new', 'Never Connected'), ('active', 'Confirmed')])
    title = fields.Selection(string='Title', selection=[('mr', 'Mr'),('ms', 'Ms'), ('mrs', 'Mrs')])
    nik = fields.Char(string='Nik')
    instansi = fields.Char(string='Instansi')



