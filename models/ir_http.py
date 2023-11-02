# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from lxml import etree
import os
import unittest
import time

import pytz
import werkzeug
import werkzeug.routing
import werkzeug.utils

from functools import partial

import odoo
from odoo import api, models
from odoo import registry, SUPERUSER_ID
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
from odoo.osv.expression import FALSE_DOMAIN
from odoo.addons.http_routing.models.ir_http import ModelConverter, _guess_mimetype
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.models.ir_http import Http

logger = logging.getLogger(__name__)


class Http(models.AbstractModel):
    _inherit = 'ir.http'


    @classmethod
    def _serve_page(cls):

        req_page = request.httprequest.path
        print ('req_pageeeeeeeeeeeeeeeeeee11113333333333333333333', req_page)

        def _search_page(comparator='='):
            page_domain = [('url', comparator, req_page)] + request.website.website_domain()
            return request.env['website.page'].sudo().search(page_domain, order='website_id asc', limit=1)

        # specific page first
        page = _search_page()
        print ('spesifi pageeeeeeeeeeeeeeeeeeeee', page.name)

        # case insensitive search
        if not page:
            page = _search_page('=ilike')
            if page:
                logger.info("Page %r not found, redirecting to existing page %r", req_page, page.url)
                return request.redirect(page.url)

        # redirect without trailing /
        if not page and req_page != "/" and req_page.endswith("/"):
            return request.redirect(req_page[:-1])

        if page:
            # prefetch all menus (it will prefetch website.page too)
            request.website.menu_id
            print ('request menu iddddddddddddddd', request.website.menu_id)

        if page and (request.website.is_publisher() or page.is_visible):
            need_to_cache = False
            cache_key = page._get_cache_key(request)
            if (
                page.cache_time  # cache > 0
                and request.httprequest.method == "GET"
                and request.env.user._is_public()    # only cache for unlogged user
                and 'nocache' not in request.params  # allow bypass cache / debug
                and not request.session.debug
                and len(cache_key) and cache_key[-1] is not None  # nocache via expr
            ):
                need_to_cache = True
                try:
                    r = page._get_cache_response(cache_key)
                    if r['time'] + page.cache_time > time.time():
                        response = werkzeug.Response(r['content'], mimetype=r['contenttype'])
                        response._cached_template = r['template']
                        response._cached_page = page
                        return response
                except KeyError:
                    pass

            _, ext = os.path.splitext(req_page)
            model_slide_channel = request.env['slide.channel'].sudo().search([('popular', '=', True)])
            
            response = request.render(page.view_id.id, {
                'deletable': True,
                'main_object': page,
                'slide_channel':model_slide_channel,
            }, mimetype=_guess_mimetype(ext))

            if need_to_cache and response.status_code == 200:
                r = response.render()
                page._set_cache_response(cache_key, {
                    'content': r,
                    'contenttype': response.headers['Content-Type'],
                    'time': time.time(),
                    'template': getattr(response, 'qcontext', {}).get('response_template')
                })
            # print ('responseeeeeeeeeeeeeeeeeeee', response)
            return response
        return False