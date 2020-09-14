from django.urls import path, include
from authentication.views import LoginAPIView,TestView,AddSubscription,VerifySubscriptionView,VerifyAccount,UserProfileView, RegistrationAPIView,UpdateProfile, AgeCategoryView,UpdateAge,Generate_Code
# ,SchoolRegistrationAPIView

app_name= 'authentication'
urlpatterns = [

    # path('verify/',VerifyAccount.as_view(),name='verify'),
    path('verify/',VerifyAccount.as_view(),name='verify'),
    path("register", RegistrationAPIView.as_view(), name='register'),
    path("login",LoginAPIView.as_view(), name='login'),
    # path("school/register",SchoolRegistrationAPIView.as_view(),name='school-register'),
    path("age/category", AgeCategoryView.as_view(),name='age-category'),
    path("update/profile/<str:id>", UpdateProfile.as_view(),name='update-profile'),
    path("view/profile/<str:id>", UserProfileView.as_view(),name='view-profile'),
    path("subscribe", AddSubscription.as_view(), name='subscribe'),
    path("verify/subscribe", VerifySubscriptionView.as_view(), name='verify-subscribe'),
    path("verify/account", TestView.as_view(), name='verif-template'),
    path("update/age", UpdateAge.as_view(), name='update-age'),
    path("generate/code", Generate_Code.as_view(), name='generate-code'),
    
    # path("school/login",SchoolLoginAPIView.as_view(),name='school-login')


]