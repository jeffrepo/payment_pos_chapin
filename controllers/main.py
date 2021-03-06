# -*- coding: utf-8 -*-
import logging
import werkzeug
import time
import requests
import urllib.request as urllib2

from werkzeug import urls

from odoo import http
from odoo.http import request, json
import hashlib
from urllib.parse import urlencode, quote_plus
import urllib

_logger = logging.getLogger(__name__)
import urllib.request
import re
import urllib.parse
from requests.utils import requote_uri
from requests.models import PreparedRequest
from urllib.parse import unquote

from datetime import timezone
import datetime
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment.controllers.portal import PaymentProcessing

class PoschapinController(http.Controller):
    # def _stripe_request(self, url, data=False, method='POST'):
    #     self.ensure_one()
    #     url = urls.url_join(self._get_stripe_api_url(), url)
    #     headers = {
    #         'AUTHORIZATION': 'Bearer %s' % self.sudo().stripe_secret_key,
    #         'Stripe-Version': '2019-05-16', # SetupIntent need a specific version
    #         }
    #     resp = requests.request(method, url, data=data, headers=headers)




    @http.route(['/payment/poschapin/s2s/create_json_3ds'], type='json', auth='public', csrf=False)
    def poschapin_s2s_create_json_3ds(self, verify_validity=False, **kwargs):
        logging.warn('TESTIING')
        logging.warn(kwargs)
        hora = int(time.time())
        logging.warn('hora')
        logging.warn(hora)

        dt = datetime.datetime.now()

        utc_time = dt.replace(tzinfo = timezone.utc)
        utc_timestamp = utc_time.timestamp()
        hora = str(int(utc_timestamp))
        logging.warn(hora)

        string_hash = "POSCHAPINTESTA1"+"|"+kwargs['amount']+"|"+hora+"|"+"YSAJRBSB_key_private_E3QY0CL0"
        logging.warn('string_hash')
        logging.warn(string_hash)
        hash = hashlib.md5(string_hash.encode('utf-8')).hexdigest()
        # hash = hashlib.md5(string_hash.encode().hexdigest())
        logging.warn('hash')
        logging.warn(hash)

        url = urls.url_join("https://pos-chapin.appspot.com/", "transaccion/json")
        logging.warn('URL')
        logging.warn(url)
        # headers = {
        #     'AUTHORIZATION': 'Bearer %s' % self.sudo().stripe_secret_key,
        #     'Stripe-Version': '2019-05-16', # SetupIntent need a specific version
        #     }
# "redirect": "http://localhost:8069/shop/confirmatio",

        data = {
            "key_public": "5834f6987a623afd644bdc1b7eb2f5c1",
            "amount": "1.00",
            "redirect": "http://localhost:8069/payment/process",
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
        # extra_url = urllib.parse.urlencode(data)
        # logging.warn(extra_url)
        token = False
        error = None
        try:
            token = request.env['payment.acquirer'].browse(int(kwargs.get('acquirer_id'))).s2s_process(kwargs)
            logging.warn('try')
            logging.warn(kwargs)
            logging.warn(token)
        except Exception as e:
            error = str(e)
        # headers = {"content-type": "x-www-form-urlencoded"}
        # json_data = json.dumps(data)
        # u = urllib.parse.quote(json_data.encode('utf-8'))
        # logging.warn('U')
        # logging.warn(u)
        #
        # resp = requests.head("https://pos-chapin.appspot.com/transaccion/json")
        # logging.warn(resp.headers)
        # resp = requests.request("POST", "https://pos-chapin.appspot.com/transaccion/json", data=dict(data=json.dumps(data)))
        # resp = requests.request("POST", "https://pos-chapin.appspot.com/transaccion/json", data=extra_url)
        #
        # logging.warn(resp)
        # requote = requote_uri(json.dumps(data, indent=4, separators=(".", " = ")))

        # logging.warn(requote)
        # urr= "https://pos-chapin.appspot.com/transaccion/json?" +str(json.dumps(data))
        # logging.warn('urr')
        # logging.warn(urr)
        # stripped = re.sub('<[^<]+?>', '', resp.text)
        # # print(stripped)
        # logging.warn(stripped)
        # logging.warn(resp.text)
        # with urllib.request.urlopen('https://pos-chapin.appspot.com/transaccion/json',data=bytes(json.dumps(headers), encoding="utf-8")) as f:
        #     print(f.read(300))
        # headers = {"content-type": "application/json"}
        # js ={'Authorization':'a74524fdcccf575b9219572978855df8','amount':'20.0'}
        # x = requests.post('https://pos-chapin.appspot.com/transaccion/json', json= js,headers=headers,verify=False)
        # js ={'key_public':'5834f6987a623afd644bdc1b7eb2f5c1'}
        # logging.warn(json.dumps(js))
        # logging.warn(kwargs['cc_number'].replace(" ", ""))


        # data = {
        #     "key_public": "5834f6987a623afd644bdc1b7eb2f5c1",
        #     "amount": "1.00",
        #     "redirect": "https://4memethod.com.gt/shop/payment",
        #     "orderid": "POSCHAPINTESTA1",
        #     "hash": hash,
        #     "time": hora,
        #     "email": "jeffer.leo93@gmail.com",
        #     "card_number": kwargs['card_number'].replace(" ", ""),
        #     "ccexp":  kwargs['ccexp'].replace(" ", ""),
        #     "cvv": kwargs['cvv'],
        #     "first_name": kwargs['first_name'],
        #     "last_name": kwargs['first_name'],
        #     "address1": "aaa",
        #     "city":"Guatemala",
        #     "state": "AA",
        #     "zip": "01018",
        #     "country": "GT",
        #     "phone": "58772265",
        # }
        # logging.warn(json.dumps(data))
        # x = requests.post('https://pos-chapin.appspot.com/transaccion/json', data= data,headers = {"content-type":"application/x-www-form-urlencoded"})
        # self.testa(data)
        # return redirect("https://pos-chapin.appspot.com/transaccion/json?"+str(dict(data=json.dumps(data))))
        # self.testa("https://pos-chapin.appspot.com/transaccion/json?"+str(f))
        # token = request.env['payment.token'].create({
        #     'name': 'test',
        #     'partner_id': int(kwargs.get('partner_id')),
        #     'acquirer_id': int(kwargs.get('acquirer_id')),
        #     'acquirer_ref': 'test'
        #
        # })
        # if token:
        #     logging.warn('el token')
        #     logging.warn(token)
        #
        # res =  {
        #             'result': True,
        #             'id': token.id,
        #             'short_name': 'test',
        #             '3d_secure': False,
        #             'verified': True,
        #         }
        # baseurl = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # kwargs['return_url'] = '/shop'
        # logging.warn('kwargs')
        # logging.warn(kwargs.get('return_url', baseurl))
        # params = {
        #     'accept_url': baseurl + '/payment/ogone/validate/accept',
        #     'decline_url': baseurl + '/payment/ogone/validate/decline',
        #     'exception_url': baseurl + '/payment/ogone/validate/exception',
        #     'return_url': kwargs.get('return_url', baseurl)
        #     }
        # tx = token.validate(**params)
        # logging.warn('tx')
        # logging.warn(tx.html_3ds)
        # res['verified'] = token.verified
        #
        # if tx and tx.html_3ds:
        #     logging.warn(tx.html_3ds)
        #     res['3d_secure'] = tx.html_3ds
        # datos = self._get_response('https://pos-chapin.appspot.com/transaccion/json',data)


        return {
                    'result': True,
                    'id': 5,
                    'short_name': 'test',
                    '3d_secure': False,
                    'verified': True,
                }

    def _get_response(self,url,data):
        req = PreparedRequest()
        req.prepare_url(url, data)
        result = requests.get(unquote(req.url)).content
        logging.warn('-getresponse')
        logging.warn(result)
        return True

    # @http.route('/payment/process', type='http', auth='user', method='POST')
    def testa(self,data):
        logging.warn('HOLA')
        # logging.warn(extra_url)
        logging.warn(kw)
        url = 'https://pos-chapin.appspot.com/transaccion/json'
        params = data
        req = PreparedRequest()
        req.prepare_url(url, params)
        logging.warn('prepare_url')
        logging.warn(unquote(req.url))
        # return werkzeug.utils.redirect(prepare_url("https://pos-chapin.appspot.com/transaccion/json",extra))

        return werkzeug.utils.redirect(unquote(req.url))

    @http.route([
        '/payment/poschapin/suc'], type='http', auth="public", methods=['POST'], csrf=False)
    def sips_dpn(self, **post):
        return werkzeug.utils.redirect('/payment/shop')


    @http.route('/shop/payment/transaccion',type="http",auth="user",website=True, csrf=False)
    def procesot_exito(self, **post):
        logging.warn('extio')
        logging.warn(post)
        orden_id = request.website.sale_get_order()
        logging.warn(orden_id)
        # transaccion_dic = {
        #     'reference': orden_id.name,
        #     'partner_id': orden_id.partner_id.id,
        #     'amount': orden_id.amount_total,
        #     'acquirer_id': 14,
        #     'sale_order_ids':  [(4, orden_id.id)],
        #     'currency_id': orden_id.currency_id.id,
        # }

        transaccion_dic = {
            'reference': orden_id.name,
            'partner_id': orden_id.partner_id.id,
            'amount': orden_id.amount_total,
            'acquirer_id': 14,
            'return_url': '/shop/payment/validate',
            'currency_id': orden_id.currency_id.id,
        }
        # transaccion_id= request.env['payment.transaction'].sudo().create(transaccion_dic)
        transaccion_id = orden_id._create_payment_transaction(transaccion_dic)
        orden_id.action_confirm()

        if orden_id.state == 'sale':

            transaccion_id._set_transaction_done()
            logging.warn('nueva transaccion')
            logging.warn(transaccion_id)
            logging.warn(transaccion_id.state)
            logging.warn(orden_id.transaction_ids)
        else:
            transaccion_id._set_transaction_cancel()

        # print (str(request.env.user.partner_id))
        return werkzeug.utils.redirect('/shop/payment/validate')

        # logging.warn(x)
        # logging.warn(x.text)
        # load = json.loads(x)
        # logging.warn(load)

        # logging.warn(x.json())
    #     self.signup()
    #
    # @http.route('/https://pos-chapin.appspot.com/transaccion/json', methods = ['POST'])
    # def signup(self):
    #
    #     return True
        # if not kwargs.get('partner_id'):
        #     kwargs = dict(kwargs, partner_id=request.env.user.partner_id.id)
        # token = False
        # error = None
        #
        # try:
        #     token = request.env['payment.acquirer'].browse(int(kwargs.get('acquirer_id'))).s2s_process(kwargs)
        # except Exception as e:
        #     error = str(e)
        #
        # if not token:
        #     res = {
        #         'result': False,
        #         'error': error,
        #     }
        #     return res
        #
        # res = {
        #     'result': True,
        #     'id': token.id,
        #     'short_name': token.short_name,
        #     '3d_secure': False,
        #     'verified': False,
        # }
        #
        # if verify_validity != False:
        #     baseurl = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #     params = {
        #         'accept_url': baseurl + '/payment/ogone/validate/accept',
        #         'decline_url': baseurl + '/payment/ogone/validate/decline',
        #         'exception_url': baseurl + '/payment/ogone/validate/exception',
        #         'return_url': kwargs.get('return_url', baseurl)
        #         }
        #     tx = token.validate(**params)
        #     res['verified'] = token.verified
        #
        #     if tx and tx.html_3ds:
        #         res['3d_secure'] = tx.html_3ds

        # return res
