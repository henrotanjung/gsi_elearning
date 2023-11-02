
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


class ResPartner(models.Model):
    _inherit = "res.partner"

    
    state = fields.Selection(compute='_compute_state', search='_search_state', string='Status',
                 selection=[('new', 'Never Connected'), ('active', 'Confirmed')])
    nik = fields.Char(string='Nik')
    instansi = fields.Char(string='Instansi')
    notifikasi = fields.Boolean('Email Notification', default=True)

    pekerjaan = fields.Selection(selection=[
        ('dokter_umum', 'Dokter Umum'),
        ('dokter_spesialis', 'Dokter Spesialis'),
        ('bidan', 'Bidan'),
        ('tenaga_kesehatan_lainnya', 'Tenaga Kesehatan Lainnya'),
        ('masyrakat_umum', 'Masyrakat Umum'),
        ('dokter', 'Dokter'),
        ('pelajar', 'Pelajar'),
        ('dosen_pengajar', 'Dosen / Pengajar'),
        ('staf_lab', 'Staf Laboratorium'),
        ('peneliti', 'Peneliti'),
        ('pekerjaan_lainnya', 'Lainnya'),
    ], string='Job Position', required=True)

    pekerjaan_lainnya = fields.Char(string='Pekerjaan Lainnya')

    type_pendaftaran = fields.Selection(string='Registration Type', selection=[('sertifikat_skp_pogi', 'Sertifikat skp pogi'), ('sertifikat_skp_dokter_umum', 'Sertifikat skp dokter umum'), ('sertifikat_tanpa_skp', 'sertifikat_tanpa_skp'), ('Non sertifikat', 'non_sertifikat')])


    referensi = fields.Selection(selection=[
        ('ig_gsilab', 'Instagram @gsilab.id'),
        ('ig_tanyadna', 'Instagram @tanyadna.id'),
        ('linkedin_gsilab', 'LinkedIn GSI Lab'),
        ('tiktok', 'Tiktok'),
        ('facebook', 'Facebook'),
        ('broadcast_wa', 'Broadcast Whatsapp'),
        ('telegram', 'Telegram'),
        ('referensi_lainnya', 'Lainnya'),
    ], string='Referensi', required=True)

    referensi_lainnya = fields.Char(string='Referensi Lainnya')




