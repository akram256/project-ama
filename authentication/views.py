import os
import secrets
import re
import requests
import jwt
import json
import logging
from datetime import timedelta, datetime, time, date
from decimal import Decimal

from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework.views import APIView

from .serializers import RegistrationSerializer,LoginSerializer,AgeSerializer,UpdateProfileSerializer,SubcriptionSerializer,VerifySubscriptionSerializer
# ,SchoolRegistrationSerializer,SchoolLoginSerializer
from authentication.models import User,Age_Category,UserProfile
# , School
from utils import services
from utils.subscription import PaystackPayment
from utils.tasks import send_user_email

logger = logging.getLogger(__name__)



class RegistrationAPIView(generics.GenericAPIView):
    """Register new users."""
    serializer_class = RegistrationSerializer
    permission_class = (AllowAny,)

    def post(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(data=request.data)
        password = request.data.get('password')
        email = request.data.get('email')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email= str(email)
        email = email.lower()
        email_pattern = services.EMAIL_PATTERN
        password_pattern = services.PASSWORD_PATTERN
        url_param = get_current_site(request).domain
        cache_key = email
        print(cache.get(cache_key))
        if cache.get(cache_key):
          
            return Response({'message': f"Please visit your email {email} to complete registration", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(password_pattern,password):
            return Response({'message':'Password is weak, please use atleast 1 UPPERCASE, 1 LOWERCASE, 1 SYMBOL',}, status=status.HTTP_400_BAD_REQUEST)
        
        if re.match(email_pattern,email):
            user = [i for i in users if i.email == email]
            if user:
                return Response({'message':'This email: {} , already belongs to a user on ama'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.info('email looks good')
        else:
            return Response({'message':'Email: {} is not valid'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            user=User(email=email,password=password,first_name=first_name,last_name=last_name,role='USER',is_new_user=True)
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user) 
            profile= UserProfile.objects.get(user=user)   
            email_verification_url=reverse('authentication:verify')
            full_url= request.build_absolute_uri(email_verification_url + '?token='+user.token)
            email_data = {'subject':'Welcome To Africa My Africa','email_from':settings.EMAIL_FROM}
            content = render_to_string('activate_account.html',{'token':'{}'.format(full_url),} )
            send_user_email.delay(email,content,**email_data)

            details = {'field':'auth','password':password,'email':email}
            logger.info(f'user {email} has been registered')
            return Response({'message': "Registration successful, Kindly check your email to activate your account", 'status': '00','token':user.token, 
            # Kindly Check your email for complete the registration
                    'user_id':user.id,
                    'profile_id':profile.id,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email':user.email,}, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccount(APIView):
    permission_classes = (AllowAny, )
    def get(self,request,format=None):
        token = request.GET['token']
        payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
        id = payload['id']
        user = User.objects.filter(id=id)
        user.update(is_active=True)
        return HttpResponseRedirect('https://ama256.herokuapp.com/api/v1/verify/account')

class TestView(TemplateView):
    def get(self, request):
        return render(request,'verify.html')

class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    queryset=User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        # new_user=User.objects.filter(email=email, is_new_user=True)
        # print(new_user)
        # if new_user.exists():
        if serializer.is_valid(raise_exception=True):
        
            user = authenticate(email=email, password=password) 
            # if user.
            if user is None:
                users = User.objects.all()
                return Response ({'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not user.is_active:
                    raise serializers.ValidationError(
                        'This account is not verified, Kindly check your email to verify account.'
                    )
                else:
                    logger.info('login successful for {}'.format(email))
            profile= UserProfile.objects.get(user=user) 

            resp ={
                    'status':'00',
                    'id':user.id,
                    'profile_id':profile.id,
                    'token':user.token,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email':user.email,
                    'is_new_user':user.is_new_user,

                    'message':'user loggedin successfully'
                }
            user.is_new_user=False
            user.save()
            return Response(resp, status=status.HTTP_200_OK)
                
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


class AgeCategoryView(ListAPIView):
    serializer_class=AgeSerializer
    permission_classes=(AllowAny,)
    queryset=Age_Category.objects.all()


    def post(self, request):
        post_data = {"age_category":request.data["age_category"],}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Age category  has been  successfully Input"},
                        status=status.HTTP_201_CREATED)
                        
class UpdateAge(RetrieveUpdateDestroyAPIView):
    permission_classes =(AllowAny,)
    serializer_class = AgeSerializer
    lookup_field = 'id'
    queryset = Age_Category.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message':'Age category has Successfully updated',
            'data':serializer.data},status=status.HTTP_200_OK)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
    lookup_field='id'
    queryset=UserProfile.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))


class UpdateProfile(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
    lookup_field = 'id'

    def get_object(self,id):        
        try:
            user = User.objects.get(id=id)
            return UserProfile.objects.get(user=user),user
        except Exception as e:
            print(e)
            return None, None

    def put(self, request,id):
        if not id:
            return Response({'message':'network error please try again', 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            userprofile = self.get_object(id)[0]
            user = self.get_object(id)[1]
            print(id)
        
        if not userprofile:
            return Response({'message':'user does not exist', 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.all()
        rdata = request.data
        first_name = request.data['user']['first_name']
        last_name=request.data['user']['first_name']
        email = request.data['user']['email']
        try:
            image=request.data['image']
        except:
            image=None
        email=email.lower()
        email_pattern = services.EMAIL_PATTERN

        if email and (email != request.user.email):
            if re.match(email_pattern,email):
                userx = [i for i in users if i.email == email]
                if userx:
                    return Response({'message':'This email: {} , already belongs to a user on ama'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    rdata['user']['email'] = email
            else:
                return Response({'message':'Email: {} is not valid'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
        else:
            rdata['user']['email'] = ''
      
        serializer = self.serializer_class(userprofile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'user profile updated','status':'00','data':serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


class AddSubscription(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = SubcriptionSerializer(data=request.data)
        if serializer.is_valid():
            resp = PaystackPayment.make_payment(amount=request.data.get('amount'),email=request.data.get('email'))
            print(request.data.get('email'))
            print(resp)
            status = resp.get('status')
            print(status)
            checkout_url = resp.get("data").get("authorization_url")
            message = (resp.get('message'))
            if status:
                return Response({'checmake_paymentkout_url':checkout_url})
        return Response({'error':message}, status=status.HTTP_400_BAD_REQUEST)


class VerifySubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = VerifySubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            resp = PaystackPayment.verify_payment(reference=request.data.get('reference'))
            print(resp)
            status = resp.get('status')
            message = resp.get('message')
            amount = resp.get("data").get("amount")
            reference = resp.get("data").get("reference")
            customer_code = resp.get("data").get("customer").get("customer_code")
            transaction_date = resp.get("data").get("transaction_date")
            if status:
                return Response({"message":"Payment Successful"})
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)



