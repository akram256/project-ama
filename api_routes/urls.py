from django.urls import path, include
from authentication.views import LoginAPIView, RegistrationAPIView,SchoolRegistrationAPIView,SchoolLoginAPIView

app_name= 'authentication'
urlpatterns = [

    # path('verify/',VerifyAccount.as_view(),name='verify'),
    path("register", RegistrationAPIView.as_view(), name='register'),
    path("login",LoginAPIView.as_view(), name='login'),
    path("school/register",SchoolRegistrationAPIView.as_view(),name='school-register'),
    path("school/login",SchoolLoginAPIView.as_view(),name='school-login')


]