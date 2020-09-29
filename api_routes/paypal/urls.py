from django.urls import path, include
from paypal.views import Payment,ApprovePaymentView,SuccessView
# ,SchoolLoginAPIView

app_name= 'paypal'
urlpatterns = [

         path('paypalpayment',Payment.as_view(),name='paypal-payment'),
         path('approval/payment',ApprovePaymentView.as_view(),name="approve-payment"),
         path('success/pay',SuccessView.as_view(),name='success-template'),
         
         

    


]