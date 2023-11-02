# -*- coding: utf-8 -*-

# Part of Odoo. See LICENSE file for full copyright and licensing details.



import base64

import functools

import json

import logging

import math

import re



from werkzeug import urls



from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID

from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied

from odoo.http import content_disposition, Controller, request, route

from odoo.tools import consteq

from odoo.addons.portal.controllers.portal import CustomerPortal



from odoo.addons.payment.controllers.portal import PaymentProcessing

from odoo.addons.portal.controllers.mail import _message_post_helper

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager



class ElearningCustomPortal(CustomerPortal):



    @route(['/my', '/my/home'], type='http', auth="user", website=True)

    def home(self, **kw):



        print ('login user', request.session.uid)

        user_login_id = request.session.uid       

        print () 

        # partner_obj = request.env['res.partner']

        user_obj = request.env['res.users']

        slide_channel_obj = request.env['slide.channel']

        

        user_data = user_obj.sudo().browse(user_login_id)



        quotations = self.get_quotation()



        

        product_ids = []

        for quotation in quotations:

            product_ids.append(quotation.order_line[0].product_id.id)





        # print ('product idssssssssssssss', product_ids)



        slide_channel_items = slide_channel_obj.sudo().search([('product_id','in', product_ids)])

        slide_channel_items_data = slide_channel_items.browse(slide_channel_items)

        # print ('slide chanel data ', slide_channel_items_data)



        product_slide_channel_ids = {}

        for quotation in quotations:

            for slide_channel_item in slide_channel_items:

                if quotation.order_line[0].product_id == slide_channel_item.product_id:

                    product_slide_channel_ids[quotation] = slide_channel_item



        # print ('slide chanellllllll idssssssssss : ',product_slide_channel_ids)



        values = self._prepare_portal_layout_values()

        values['user'] = user_data

        values['quotations'] = quotations

        values['slide_quotations'] = product_slide_channel_ids

        

        return request.render("gsi_elearning.user_profile_templates", values)

    

    def _prepare_quotations_domain(self, partner):

        return [

            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),

            ('state', 'in', ['sent', 'cancel'])

        ]



    def _get_sale_searchbar_sortings(self):

        return {

            'date': {'label': _('Order Date'), 'order': 'date_order desc'},

            'name': {'label': _('Reference'), 'order': 'name'},

            'stage': {'label': _('Stage'), 'order': 'state'},

        }

    

    def get_quotation(self):

        values = self._prepare_portal_layout_values()

        partner = request.env.user.partner_id

        SaleOrder = request.env['sale.order']



        domain = self._prepare_quotations_domain(partner)



        searchbar_sortings = self._get_sale_searchbar_sortings()



        sortby = 'date'

        sort_order = searchbar_sortings[sortby]['order']



        # if date_begin and date_end:

        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]



        # count for pager

        quotation_count = SaleOrder.search_count(domain)

        page = 1

        

        print ('domainnnnn', domain)

        quotations = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page)

        # request.session['my_quotations_history'] = quotations.ids[:100]



        # values.update({

        #     # 'date': date_begin,

        #     'quotations': quotations.sudo(),

        #     'page_name': 'quote',

        #     'default_url': '/my/quotes',

        #     'searchbar_sortings': searchbar_sortings,

        #     'sortby': sortby,

        # })



        return quotations

    
