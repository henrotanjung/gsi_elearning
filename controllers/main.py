# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import babel.messages.pofile
import base64
import copy
import datetime
import functools
import glob
import hashlib
import io
import itertools
import jinja2
import json
import logging
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from collections import OrderedDict, defaultdict, Counter
from werkzeug.urls import url_encode, url_decode, iri_to_uri
from lxml import etree
import unicodedata
import odoo
import odoo.modules.registry
from odoo.api import call_kw, Environment
from odoo.modules import get_module_path, get_resource_path
from odoo.tools import image_process, topological_sort, html_escape, pycompat, ustr, apply_inheritance_specs, lazy_property
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.translate import _
from odoo.tools.misc import str2bool, xlsxwriter, file_open
from odoo.tools.safe_eval import safe_eval, time
from odoo import http, tools
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception, Response
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.models import check_method_name
from odoo.service import db, security
import logging
import werkzeug
from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home #, SIGN_UP_REQUEST_PARAMS
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website.controllers.main import Website
from odoo.addons.web.controllers.main import Home
_logger = logging.getLogger(__name__)
# # Shared parameters for all login/signup flows
# SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
#                           'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
#                           'password', 'confirm_password', 'city', 'country_id', 'lang'}
# class HomeElearning(Home):
#     @http.route('/web/login', type='http', auth="none")
#     def web_login(self, redirect=None, **kw):
#         print ('abcccccccccccc')
#         ensure_db()
#         request.params['login_success'] = False
#         if request.httprequest.method == 'GET' and redirect and request.session.uid:
#             return http.redirect_with_hash(redirect)
#         if not request.uid:
#             request.uid = odoo.SUPERUSER_ID
#         values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
#         try:
#             values['databases'] = http.db_list()
#         except odoo.exceptions.AccessDenied:
#             values['databases'] = None
#         if request.httprequest.method == 'POST':
#             old_uid = request.uid
#             try:
#                 uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
#                 request.params['login_success'] = True
#                 return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
#             except odoo.exceptions.AccessDenied as e:
#                 request.uid = old_uid
#                 if e.args == odoo.exceptions.AccessDenied().args:
#                     values['error'] = _("Wrong login/password")
#                 else:
#                     values['error'] = e.args[0]
#         else:
#             if 'error' in request.params and request.params.get('error') == 'access':
#                 values['error'] = _('Only employees can access this database. Please contact the administrator.')
#         if 'login' not in values and request.session.get('auth_login'):
#             values['login'] = request.session.get('auth_login')
#         if not odoo.tools.config['list_db']:
#             values['disable_database_manager'] = True
#         # response = request.render('web.login', values)  # saat ini ganti di custom ku, jika dari custom beda behaviour, ganti di sini aja templatenya
#         response = request.render('gsi_elearning.login_templates', values)
#         response.headers['X-Frame-Options'] = 'DENY'
#         print ('responseeeeeeeeeee1111', dir(response))
#         print ('responseeeeeeeeeee', dir(response.data))
#         return response
class AuthSignupHomeElearning(AuthSignupHome):
    @http.route()
    def web_login(self, *args, **kw):
        print (55555)
        ensure_db()
        response = super(AuthSignupHomeElearning, self).web_login(*args, **kw)
        response.qcontext.update(self.get_auth_signup_config())
        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get('redirect'))
        return response
    
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        values_update_partner = { key: qcontext.get(key) for key in ('phone', 'instansi', 'function', 'notifikasi', 'pekerjaan', 'pekerjaan_lainnya', 'referensi', 'referensi_lainnya') }
        values_update_partner['title'] = qcontext.get('title_field', 3)
        
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values, values_update_partner)
        request.env.cr.commit()
    def _signup_with_values(self, token, values, values_update_partner):
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        new_commit = request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
        uid = request.session.authenticate(db, login, password)
        if uid:
            # pass
            new_partner = request.env['res.users'].browse(uid).partner_id
            new_partner.sudo().write(values_update_partner)
            ### keterangan nanti write di sini partner nya, karena respatner otomatis di create 
            ### ketika create res user , karena res user inherit res.partner. itu sudah aturan odoo
            ### untuk field2 yg di parsing dari website ketika sign up perlu di rubah dari sini : SIGN_UP_REQUEST_PARAMS
            ### karena itu disitu di setting semua. namun yg ke model res user tetap, tidak boleh di rubah
            ### karena bikin error. cukup yg ke respartner ketika write setelah di create berhasil. 
            ### create user disana pakai method copy
            # request.env
            # product_id = self.env['product.product'].browse(product_id)
            
            print ('new user created browse', new_partner)
        if not uid:
            raise SignupError(_('Authentication Failed.'))
class WebsiteElearning(Website):
    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        print ('home page .......')
        slide_obj = request.env['slide.channel']
        courses = slide_obj.sudo().search([])
        popular_programs = []
        all_courses = []  
        courses_home_page = []
        training_workshops = []
        events = []
        for p in courses:
            if p.popular:
                popular_programs.append(p)
            if p.type_event == 'training_workshop' and p.home_page:
                training_workshops.append(p)            
            if p.type_event == 'course' and p.home_page:
                courses_home_page.append(p)
            if p.type_event == 'event' and p.home_page:
                events.append(p)
                
            all_courses.append(p)
        
        print ('courses home pageeeeeeeeee ....', courses_home_page)
        return http.request.render('gsi_elearning.elearning_website_new', {'popular_programs': popular_programs, 'courses_home_page': courses_home_page, 'training_workshops': training_workshops, 'events': events, 'all_courses': all_courses, 'uid' : request.uid})
        raise request.not_found()
    
    @http.route('/web/course', type='http', auth="public", website=True, sitemap=True)
    def course_elearning(self, **kw):
        print ('page courseeeeeeeeeeeee', request.uid)
        slide_obj = request.env['slide.channel']
        courses = slide_obj.sudo().search([])
        popular = []      
        all_courses = []  
        for p in courses:
            if p.popular:
                popular.append(p)
            all_courses.append(p)
        
        return http.request.render('gsi_elearning.course_templates', {'popular': popular, 'all_courses': all_courses, 'uid' : request.uid})
    
    @http.route('/web/training_workshop', type='http', auth="public", website=True, sitemap=True)
    def training_workshop(self, **kw):
        print ('page training')
        return http.request.render('gsi_elearning.training_workshop', {'uid' : request.uid})
    
    @http.route('/web/event', type='http', auth="public", website=True, sitemap=True)
    def event(self, **kw):
        print ('page event')
        return http.request.render('gsi_elearning.event_elearning_template', {'uid' : request.uid})
    @http.route('/web/about', type='http', auth="public", website=True, sitemap=True)
    def about(self, **kw):
        print ('page about')
        return http.request.render('gsi_elearning.about', {'uid' : request.uid})
    @http.route('/web/blog', type='http', auth="public", website=True, sitemap=True)
    def blog(self, **kw):
        print ('page blog')
        return http.request.render('gsi_elearning.blog_elearning_template', {'uid' : request.uid})
    @http.route('/web/about', type='http', auth="public", website=True, sitemap=True)
    def about(self, **kw):
        print ('page about')
        return http.request.render('gsi_elearning.about_elearning_template', {'uid' : request.uid})
        
    
    
    