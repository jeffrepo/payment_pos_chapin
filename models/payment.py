# coding: utf-8

import logging
import requests
import pprint
from requests.exceptions import HTTPError
from werkzeug import urls
from collections import namedtuple

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round

from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment_stripe.controllers.main import StripeController


from odoo.addons.payment_pos_chapin.controllers.main import PoschapinController
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, ustr
from odoo.tools.float_utils import float_compare, float_repr, float_round
import datetime
import hashlib
from urllib.parse import urlencode, quote_plus
from datetime import timezone
import time
_logger = logging.getLogger(__name__)

from requests.models import PreparedRequest
from urllib.parse import unquote

# The following currencies are integer only, see https://stripe.com/docs/currencies#zero-decimal
INT_CURRENCIES = [
    u'BIF', u'XAF', u'XPF', u'CLP', u'KMF', u'DJF', u'GNF', u'JPY', u'MGA', u'PYG', u'RWF', u'KRW',
    u'VUV', u'VND', u'XOF'
]


class PaymentAcquirerStripe(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('poschapin', 'Pos chapin')])
    key_public = fields.Char("Llave publica")
    poschapin_image_url = fields.Char(
        "URL", groups='base.group_user')


    def poschapin_get_form_action_url(self):
        self.ensure_one()
        logging.warn('funcion URL')
        return {'url': 'www.google.com'}


    def obtener_url(self,kwargs):
        logging.warn(kwargs)
        kwargs = kwargs[0]
        dt = datetime.datetime.now()

        utc_time = dt.replace(tzinfo = timezone.utc)
        utc_timestamp = utc_time.timestamp()
        hora = str(int(utc_timestamp))
        logging.warn(hora)

        string_hash = "POSCHAPINTESTA1"+"|"+kwargs['amount']+"|"+hora+"|"+"YSAJRBSB_key_private_E3QY0CL0"
        logging.warn('string_hash')
        logging.warn(string_hash)

        hash = hashlib.md5(string_hash.encode('utf-8')).hexdigest()
        logging.warn('hash')
        logging.warn(hash)

        #"redirect": "http://localhost:8069/shop/payment/validate",
        data = {
            "key_public": "5834f6987a623afd644bdc1b7eb2f5c1",
            "amount": "1.00",
            "redirect": "http://localhost:8069/shop/payment/transaccion",
            "orderid": "POSCHAPINTESTA1",
            "hash": hash,
            "time": hora,
            "email": "jeffer.leo93@gmail.com",
            "card_number": kwargs['card_number'].replace(" ", ""),
            "ccexp":  kwargs['ccexp'].replace(" / ", ""),
            "cvv": kwargs['cvv'],
            "first_name": kwargs['first_name'],
            "last_name": kwargs['first_name'],
            "address1": "aaa",
            "city":"Guatemala",
            "state": "AA",
            "zip": "01018",
            "country": "GT",
            "phone": "58772265",
        }

        url = 'https://pos-chapin.appspot.com/transaccion/json'
        params = data
        req = PreparedRequest()
        req.prepare_url(url, params)
        logging.warn('prepare_url')
        logging.warn(unquote(req.url))


        # logging.warn('en f')
        # logging.warn(self.website.sale_get_order())
        logging.warn(unquote(req.url))
        return unquote(unquote(req.url))

    # def visanet_form_generate_values(self, values):
    #     reference = '{}|{}'.format(values['reference'], request.session.sid)
    #     logging.warn('REFERENCE')
    #     logging.warn(reference)
    #     return True

class PaymentToken(models.Model):
    _inherit = 'payment.token'

    def poschapin_create(self, values):
        logging.warn('poschapin_create')
        logging.warn(values)
        if values.get('card_number'):
            logging.warn('adssad')
            # create a alias via batch
        return {}
