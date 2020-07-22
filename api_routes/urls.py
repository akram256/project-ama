from django.urls import path, include
from authentication.views import LoginAPIView,AddSubscription,VerifySubscriptionView,PaystackInfo,VerifyAccount,UserProfileView, RegistrationAPIView,UpdateProfileView,SchoolRegistrationAPIView, AgeCategoryView
# ,SchoolLoginAPIView

app_name= 'authentication'
urlpatterns = [

    # path('verify/',VerifyAccount.as_view(),name='verify'),
    path('verify/',VerifyAccount.as_view(),name='verify'),
    path("register", RegistrationAPIView.as_view(), name='register'),
    path("login",LoginAPIView.as_view(), name='login'),
    path("school/register",SchoolRegistrationAPIView.as_view(),name='school-register'),
    path("age/category", AgeCategoryView.as_view(),name='age-category'),
    path("update/profile/<str:id>", UpdateProfileView.as_view(),name='update-profile'),
    path("view/profile/<str:id>", UserProfileView.as_view(),name='view-profile'),
    path("paystack", PaystackInfo.as_view(), name='paystack'),
    path("subscribe", AddSubscription.as_view(), name='subscribe'),
    path("verify/subscribe", VerifySubscriptionView.as_view(), name='verify-subscribe'),



   
    # path("school/login",SchoolLoginAPIView.as_view(),name='school-login')


]