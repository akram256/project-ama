import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PaystackPayment:

    @classmethod
    def make_payment(cls, amount,email, service_email=None):
        if not service_email:
            service_email = settings.CUSTOMER_SERVICE_EMAIL
        response = requests.post('https://api.paystack.co/transaction/initialize',
            data={
                'amount': int(amount) * 100, #converting to kobo
                'email': email,
                'customer': {
                    'email': service_email
                },
                "callback_url": "http://138bb805.ngrok.io"
            },
            headers={
                'Authorization': 'Bearer {}'.format(settings.PAYSTACK_SECRET_KEY),
            }
        )
        if response.status_code == 200:
            logger.info("Paystack generated url successful. {} ".format(response.json()))
            return response.json()
        logger.error("Error occured calling paystack. {} ".format(response.json()))
        return response.json()

    @classmethod
    def verify_payment(cls, reference):
        response = requests.get("https://api.paystack.co/transaction/verify/{}".format(reference),
                headers={
                'Authorization': 'Bearer {}'.format(settings.PAYSTACK_SECRET_KEY),
                "content-type": "application/json",
                "cache-control": "no-cache"
            }
        )

        if response.status_code == 200:
            logger.info("Payment verified. {}".format(response.json()))
            return response.json()
        logger.error("Payment was unable to be verified. {}".format(response.json()))
        return response.json()
    

