from django.urls import path, include
from authentication.views import LoginAPIView, RegistrationAPIView

app_name= 'authentication'
urlpatterns = [

    # path('verify/',VerifyAccount.as_view(),name='verify'),
    path("register", RegistrationAPIView.as_view(), name='register'),
    path("login",LoginAPIView.as_view(), name='login'),


]