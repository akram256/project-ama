import requests
from django.conf import settings
import logging
import base64
import json
from store.models import Store

logger = logging.getLogger(__name__)

class PayPalPayment:

    @classmethod
    def Payment(self,product, price):
        client_ID= settings.CLIENT_ID
        client_Secret=settings.CLIENT_SECRET
        
        # if not product:id
      
        print(product)
        data={
            "intent": "sale",
            "payer": {
            "payment_method": "paypal"
            },
            "transactions": [{
            "amount": {
                "total": price,
                "currency": "USD",
                "details": {
                "subtotal": price,
                # "tax": "0.07",
                # "shipping": "0.03",
                # "handling_fee": "1.00",
                # "shipping_discount": "-1.00",
                # "insurance": "0.01"
                }
            },
            # "description": "This is the payment transaction description.",
            # # "custom": "EBAY_EMS_90048630024435",
            # # "invoice_number": "48787589673",
            # "payment_options": {
            #     "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
            # },
            "item_list": {
                "items": [{
                "name": "product",
                # "description": "Brown color hat",
                "quantity": "5",
                "price": "500",
                # "tax": "0.01",
                # "sku": "1",
                "currency": "USD"
                }
                   , 
                {
                "name": "handbag",
                "description": "Black color hand bag",
                "quantity": "1",
                "price": "500",
                # "tax": "0.02",
                # "sku": "product34",
                "currency": "USD"
                }
                ]},
             
                
            #     # "shipping_address": {
            #     # "recipient_name": "Hello World",data":json.dumps(data)
            #     # "line1": "4thFloor",
            #     # "line2": "unit#34",
            #     # "city": "SAn Jose",
            #     # "country_code": "US",
            #     # "postal_code": "95131",
            #     # "phone": "011862212345678",
            #     # "state": "CA"
            #     # }
            # }
            }],
            "note_to_payer": "Contact us for any questions on your order.",
            "redirect_urls": {
            "return_url": "http://c9df060f00b0.ngrok.io/api/v1/approval/payment",
            "cancel_url": "http://c9df060f00b0.ngrok.io/api/v1/"
            }
            
            }
            # "purchase_units": [
            #     {
            #     "amount": {
            #         "currency_code": "USD",
            #         "value": price
            # # 'product': product,
            # 'price': price,
            # "return_url": "http://138bb805.ngrok.io",
        #     # "cancel_url": "http://138bb805.ngrok.io"
        # },"purchase_units": [
        #     #     {
        #     #     "amount": {
        #     #         "currency_code": "USD",
        #     #         "value": price
        #     # # 'product': product,
        #         }
        #     ]
        # }
            
        headers =  {"Content-Type": "application/json","Authorization": "Basic {0}".format(base64.b64encode((client_ID + ":" + client_Secret).encode()).decode())}
        attrib = {"url":"https://api.sandbox.paypal.com/v1/payments/payment","headers":headers, "data":json.dumps(data),}
        response = getattr(requests,"post")(**attrib)
        if response.status_code == 201:
            logger.info("Paypal order successfully created. {} ".format(response.json()))
            return response.json()
        logger.error("Error occured calling paypal. {} ".format(response.json()))
        return response.json()

    @classmethod
    def approve_payment(self,payer_id,payid):
        client_ID= settings.CLIENT_ID
        client_Secret=settings.CLIENT_SECRET

        data={
            "payer_id":payer_id,
        }
        print(payer_id)

        headers =  {"Content-Type": "application/json","Authorization": "Basic {0}".format(base64.b64encode((client_ID + ":" + client_Secret).encode()).decode())}
        attrib = {"url":" https://api.sandbox.paypal.com/v1/payments/payment/{}/execute".format(payid),"headers":headers, "data":json.dumps(data),}
        response = getattr(requests,"post")(**attrib)
        # print(response)
  
        if response.status_code == 200:
            logger.info("Payment verified. {}".format(response.json()))
            return response.json()
        logger.error("Payment was unable to be verified. {}".format(response.json()))
        return response.json()
    



