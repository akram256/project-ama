from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .paymentservice import PayPalPayment
from .serializers import PaypalSerializer


# Create your views here.

class Payment(ListAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = PaypalSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            resp = PayPalPayment.Payment(product=request.data.get('product'))
            status = resp.get('status')
            checkout_url = resp.get("data").get("authorization_url")
            message = (resp.get('message'))
            if status:
                return Response({'checkout_url':checkout_url})
        # message = (resp.get('message'))
        return Response({'error':message}, status=status.HTTP_400_BAD_REQUEST)

