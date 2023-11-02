# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _



class ChannelElearning(models.Model):
    _inherit = 'slide.slide'
    
    @api.onchange('datas')
    def _on_change_datas(self):
        """ For PDFs, we assume that it takes 5 minutes to read a page.
            If the selected file is not a PDF, it is an image (You can
            only upload PDF or Image file) then the slide_type is changed
            into infographic and the uploaded dataS is transfered to the
            image field. (It avoids the infinite loading in PDF viewer)"""
        print ('in to function remark')
        # I remark this function, since the pydf2 library is not working. and this method is not realy important. because it is only an onchange method.
        # this is an alternatif solution. for the next i need to figure out why the library is not working on production. on local its working fine but not using docker.
        pass
        