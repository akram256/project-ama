from django.urls import path, include
from paypal.views import Payment
# ,SchoolLoginAPIView

app_name= 'paypal'
urlpatterns = [

         path('paypalpayment',Payment.as_view(),name='paypal-payment'),

    


]