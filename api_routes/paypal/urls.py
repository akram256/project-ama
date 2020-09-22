from django.urls import path, include
from paypal.views import Payment,ExecutePaymentView,ApprovePaymentView
# ,SchoolLoginAPIView

app_name= 'paypal'
urlpatterns = [

         path('paypalpayment',Payment.as_view(),name='paypal-payment'),
         path('execute/payment',ExecutePaymentView.as_view(),name='execute-payment'),
         path('approval/payment',ApprovePaymentView.as_view(),name="approve-payment")
         

    


]