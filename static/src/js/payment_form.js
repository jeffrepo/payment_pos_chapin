odoo.define('payment_pos_chapin.payment_form', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');
var PaymentForm = require('payment.payment_form');
var rpc = require('web.rpc');

var _t = core._t;

PaymentForm.include({

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * called when clicking on pay now or add payment event to create token for credit card/debit card.
     *
     * @private
     * @param {Event} ev
     * @param {DOMElement} checkedRadio
     * @param {Boolean} addPmEvent
     */
    _createAuthorizeTokenPos: function (ev, $checkedRadio, addPmEvent) {
        var self = this;
        console.log('_createAuthorizeTokenPos');

        if (ev.type === 'submit') {
            var button = $(ev.target).find('*[type="submit"]')[0]
        } else {
            var button = ev.target;
        }
        var acquirerID = this.getAcquirerIdFromRadio($checkedRadio);
        var acquirerForm = this.$('#o_payment_add_token_acq_' + acquirerID);
        var inputsForm = $('input', acquirerForm);
        var formData = self.getFormData(inputsForm);
        if (this.options.partnerId === undefined) {
            console.warn('payment_form: unset partner_id when adding new token; things could go wrong');
        }
        var AcceptJs = false;
        if (formData.acquirer_state === 'enabled') {
            AcceptJs = 'https://js.authorize.net/v3/AcceptUI.js';
        } else {
            AcceptJs = 'https://jstest.authorize.net/v3/AcceptUI.js';
        }

        // if (formData.acquirer_state === 'enabled') {
        //     AcceptJs = 'https://js.authorize.net/v3/AcceptUI.js';
        // } else {
        //     AcceptJs = 'https://jstest.authorize.net/v3/AcceptUI.js';
        // }
        console.log(formData)

        console.log('addPMSS')
        console.log($checkedRadio)
        console.log(addPmEvent)
        // window.location = 'https://stackoverflow.com/questions/4827740/load-web-pages-with-ajax';





        window.responseHandler = function (response) {
            _.extend(formData, response);
            console.log('click')

            var dic = {
                'hola': 'test',
                'card_number': '4111 1111 1111 1111',
                'ccexp':'09 / 22',
                'cvv':'685',
                'first_name':'jeff',
                'amount': '1.00',

            }
            rpc.query({
                model: 'payment.acquirer',
                method: 'obtener_url',
                args: [[],[dic]],
            }).then(function (urls) {
                console.log(urls)
                window.location = urls;
            });

            // if (response.messages.resultCode === "Error") {
            //     var errorMessage = "";
            //     _.each(response.messages.message, function (message) {
            //         errorMessage += message.code + ": " + message.text;
            //     })
            //     acquirerForm.removeClass('d-none');
            //     return self.displayError(_t('Server Error'), errorMessage);
            // }

        //     self._rpc({
        //         route: formData.data_set,
        //         params: formData
        //     }).then (function (data) {
        //         if (addPmEvent) {
        //             if (formData.return_url) {
        //                 window.location = formData.return_url;
        //             } else {
        //                 window.location.reload();
        //             }
        //         } else {
        //             $checkedRadio.val(data.id);
        //             self.el.submit();
        //         }
        //     }).guardedCatch(function (error) {
        //         // if the rpc fails, pretty obvious
        //         error.event.preventDefault();
        //         acquirerForm.removeClass('d-none');
        //         self.displayError(
        //             _t('Server Error'),
        //             _t("We are not able to add your payment method at the moment.") +
        //                 self._parseError(error)
        //         );
        //     });
        };

        // ajax.loadJS(AcceptJs).then(function () {
        //     self.$button.trigger('click');
        // });

        if (this.$button === undefined) {
            console.log('undefine button')
            var params = {
                'class': 'AcceptUI d-none',
                'data-apiLoginID': formData.login_id,
                'data-clientKey': formData.client_key,
                'data-billingAddressOptions': '{"show": false, "required": false}',
                'data-responseHandler': 'responseHandler'
            };
            this.$button = $('<button>', params);
            this.$button.appendTo('body');
        }
        ajax.loadJS(AcceptJs).then(function () {
            self.$button.trigger('click');
        });
    },
    /**
     * @override
     */
    updateNewPaymentDisplayStatus: function () {
        var $checkedRadio = this.$('input[type="radio"]:checked');

        if ($checkedRadio.length !== 1) {
            return;
        }

        //  hide add token form for authorize
        if ($checkedRadio.data('provider') === 'poschapin' && this.isNewPaymentRadio($checkedRadio)) {
            this.$('[id*="o_payment_add_token_acq_"]').addClass('d-none');
        } else {
            this._super.apply(this, arguments);
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    payEvent: function (ev) {
        ev.preventDefault();
        var $checkedRadio = this.$('input[type="radio"]:checked');
        console.log('pagar');
        // first we check that the user has selected a authorize as s2s payment method
        if ($checkedRadio.length === 1 && this.isNewPaymentRadio($checkedRadio) && $checkedRadio.data('provider') === 'poschapin') {
            console.log('si')
            this._createAuthorizeTokenPos(ev, $checkedRadio);

        } else {
            console.log('no')
            this._super.apply(this, arguments);
        }
    },
    /**
     * @override
     */
    addPmEvent: function (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        var $checkedRadio = this.$('input[type="radio"]:checked');
        console.log('pagar 2');
        // first we check that the user has selected a authorize as add payment method
        if ($checkedRadio.length === 1 && this.isNewPaymentRadio($checkedRadio) && $checkedRadio.data('provider') === 'poschapin') {
            this._createAuthorizeTokenPos(ev, $checkedRadio, true);
        } else {
            this._super.apply(this, arguments);
        }
    },
});
});
