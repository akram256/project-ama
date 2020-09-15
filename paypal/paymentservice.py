import requests
from django.conf import settings
import logging
import base64

logger = logging.getLogger(__name__)

class PayPalPayment:

    @classmethod
    def PaypalToken(client_ID, client_Secret):
        client_ID= settings.CLIENT_ID
        client_Secret=settings.CLIENT_SECRET
        url = "https://api.sandbox.paypal.com/v1/oauth2/token"
        data = {
                    "client_id":client_ID,
                    "client_secret":client_Secret,
                    "grant_type":"client_credentials"
                }
        headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Autin django rest frameworkhorization": "Basic {0}".format(base64.b64encode((client_ID + ":" + client_Secret).encode()).decode())
                }

        token = requests.post(url, data, headers=headers)
        return token

    @classmethod
    def Payment(product):
        client_ID= settings.CLIENT_ID
        client_Secret=settings.CLIENT_SECRET
        if not product:
            product = Cart.objects.filter(product=product)

        response = requests.post( 'https://api.sandbox.paypal.com/v2/checkout/orders',
        data={
            'product': product, #converting to kobo
            # 'price': price,
            "return_url": "http://138bb805.ngrok.io",
            "cancel_url": "http://138bb805.ngrok.io"
        },
      
        # headers = {"Content-Type": "application/json", "Authorization": 'Bearer' +token}
        headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Autin django rest frameworkhorization": "Basic {0}".format(base64.b64encode((client_ID + ":" + client_Secret).encode()).decode())
                }
        )
        print(response)
        if response.status_code == 200:
            logger.info("Paypal order successful. {} ".format(response.json()))
            return response.json()
        logger.error("Error occured calling paypal. {} ".format(response.json()))
        return response.json()


