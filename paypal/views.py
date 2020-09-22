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
            print(resp, 'here')
            # print(resp ["links"][2]["href"], "herrere")
            state=resp ["state"]
            checkout_url = resp ["links"][1]
            payID=resp["id"]
            # print(payID, 'id is here')
           
            # print(resp2)
          
            # print(full_url)
          
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
        # products = Cart.objects.filter(user=request.user.id)
        products= Cart.objects.all()
        return products 

    def get(self, request,):
        if request.user:
            data=self.get_queryset(request)
            serializer = self.serializer_class(data, many=True)
            return Response({
                'status': '00',
                # 'data':  serializer.data,
                'Message':"Payment approved"
            })
        return Response({
            'status': 99,
            'message': 'Unauthenticated!'
        }, status=status.HTTP_200_OK)


class ExecutePaymentView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # here=reverse('paypal:approve-payment')
        # full_url= request.build_absolute_uri(here)
        # print(here.get('resp'))
        resp = PayPalPayment.approve_payment(payid="PAYID-L5VAAVA5WK19181JC308871V",payer_id="DZW2RDSMTU2KQ")
        print(resp)
        state=resp ["state"]
        if state == "approved":
            return Response({"message":"Payment Successful"})
        return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)




