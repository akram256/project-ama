import requests

from django.shortcuts import render
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .paymentservice import PayPalPayment
from .serializers import PaypalSerializer,ApprovePaymentSerializer
from store.models import Cart
from store.serializers import CartSerializer


# Create your views here.

class Payment(ListAPIView):
    serializer_class=PaypalSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        post_data = {"price":request.data["price"],"product":request.data["product"]}
        serializer = self.get_serializer(data=post_data)
        print(serializer.is_valid())
        if serializer.is_valid():
            resp = PayPalPayment.Payment(price= post_data['price'],product= post_data['product'])

            state=resp ["state"]
            checkout_url = resp ["links"][1]
            payID=resp["id"]
            PayPalPayment.approve_payment(payid=payID, payer_id="84XWDTVS959S8")
            if state == "created":
                
                
                 return Response({'approval-url':checkout_url, 
                                  'ID':payID
                                  }, status=status.HTTP_201_CREATED)
           
        return Response({'error':"error"}, status=status.HTTP_400_BAD_REQUEST)

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




