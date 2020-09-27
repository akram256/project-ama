import requests

from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .paymentservice import PayPalPayment
# from .serializers import PaypalSerializer,ApprovePaymentSerializer
from store.models import Cart
from store.serializers import CartSerializer,PaymentCartSerializer
from utils.tasks import send_user_email


# Create your views here.

class Payment(ListAPIView):
    serializer_class=PaymentCartSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        products = Cart.objects.filter(user=request.user)
        # serializer = self.serializer_class(products, many=True)
        # print(serializer)
        if products.exists():
            products_amount=products.values("product__price")
            total_amount = lambda x : sum([float(data['product__price']) for data in x])
            resp = PayPalPayment.Payment(price= str(total_amount(products_amount)))
            template_data={"price":str(total_amount(products_amount))}
            email_data = {'subject':'Payment Details','email_from':settings.EMAIL_FROM}
            content = render_to_string('paypal.html',template_data)
            send_user_email.delay(request.user.email,content,**email_data)
            products.delete()
            state=resp ["state"]
            checkout_url = resp ["links"][1]
          
            if state == "created":
                    return Response({'approval-url':checkout_url, 
                                    }, status=status.HTTP_201_CREATED)
        return Response({'error':"This Transactions can not be completed. No Products in the cart at the moments"}, status=status.HTTP_400_BAD_REQUEST)

class ApprovePaymentView(ListAPIView):
    permission_classes=(AllowAny,)
    serializer_class=(CartSerializer)

    def get_queryset(self,request, *args, **kwargs):
        products= Cart.objects.all()
        return products 

    def get(self, request,):
        paymentid=request.GET.get('paymentId')
        PayerID=request.GET.get('PayerID')
        resp = PayPalPayment.approve_payment(payid=paymentid,payer_id=PayerID)
        state=resp ["state"]
        if state == "approved":
            return Response({"message":"Payment Successful"})
        return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)




