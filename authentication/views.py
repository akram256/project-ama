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
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework.views import APIView

from .serializers import RegistrationSerializer,LoginSerializer,AgeSerializer
# ,SchoolRegistrationSerializer,SchoolLoginSerializer
from authentication.models import User,Age_Category
# , School
from utils import services

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
        print(email)
        email = email.lower()
        email_pattern = services.EMAIL_PATTERN
        password_pattern = services.PASSWORD_PATTERN
        url_param = get_current_site(request).domain

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
            user=User(email=email,password=password,first_name=first_name,last_name=last_name,is_active=True,role='USER')
            user.set_password(password)
            user.save()
            # email_verification_url=reverse('Auth:verify')
            # full_url= request.build_absolute_uri(email_verification_url + '?token='+user.token)
            # email_data = {'subject':'Welcome To Africa My Africa','email_from':settings.EMAIL_FROM}
            # content = render_to_string('activate_accountregister.html',{'token':'{}'.format(full_url),} )
            # send_user_email.delay(email,content,**email_data)
            details = {'field':'auth','password':password,'email':email}
            logger.info(f'user {email} has been registered')
            return Response({'message': "Registration successful", 'status': '00','token':user.token, 
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email':user.email,}, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)



class SchoolRegistrationAPIView(generics.GenericAPIView):

    """Register new school users."""

    serializer_class = RegistrationSerializer
    permission_class = (AllowAny,)

    def post(self, request):
        school_users = User.objects.all()
        serializer = self.serializer_class(data=request.data)
        password = request.data.get('password')
        email = request.data.get('email')
        school_name=request.data.get('school_name')
        school_address=request.data.get('school_address')
        email= str(email)
        print(email)
        email = email.lower()
        email_pattern = services.EMAIL_PATTERN
        password_pattern = services.PASSWORD_PATTERN
        url_param = get_current_site(request).domain

        if not re.match(password_pattern,password):
            return Response({'message':'Password is weak, please use atleast 1 UPPERCASE, 1 LOWERCASE, 1 SYMBOL',}, status=status.HTTP_400_BAD_REQUEST)
        
        if re.match(email_pattern,email):
            user = [i for i in school_users if i.email == email]
            if user:
                return Response({'message':'This email: {} , already belongs to a user on ama'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.info('email looks good')
        else:
            return Response({'message':'Email: {} is not valid'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            user=User(email=email,password=password,school_name=school_name,school_address=school_address,is_active=True,role='SCHOOL')
            user.set_password(password)
            user.save()
            print(user,'hewre we are')
            # email_verification_url=reverse('Auth:verify')
            # full_url= request.build_absolute_uri(email_verification_url + '?token='+user.token)
            # email_data = {'subject':'Welcome To Africa My Africa','email_from':settings.EMAIL_FROM}
            # content = render_to_string('activate_account.html',{'token':'{}'.format(full_url),} )
            # send_user_email.delay(email,content,**email_data)
            details = {'field':'auth','password':password,'email':email}
            logger.info(f'user {email} has been registered')
            return Response({'message': "School Registration successful", 'status': '00',
                             'token':user.token,
                            #  'school_name':school.school_name,
                            #  'school_address':school.school_address,
                            #  'email':school.school_email,
                             }, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')

        if serializer.is_valid(raise_exception=True):
            user = authenticate(email=email, password=password) 
            if user is None:
                users = User.objects.all()
                return Response ({'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not user.is_active:
                    raise serializers.ValidationError(
                        'This user has been deactivated.'
                    )
                else:
                    logger.info('login successful for {}'.format(email))

            resp ={
                    'status':'00',
                    'token':user.token,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'email':user.email,

                    'message':'user loggedin successfully'
                }
            return Response(resp, status=status.HTTP_200_OK)
                
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


# class SchoolLoginAPIView(APIView):
#     """
#     Logs in an existing school user.
#     """
#     permission_classes = [AllowAny]
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if serializer.is_valid(raise_exception=True):
           
#             user= authenticate(email=email,password=password)

#             if user is None:
#                 users = User.objects.all()
#                 return Response ({'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 if not user.is_active:
#                     raise serializers.ValidationError(
#                         'This user has been deactivated.'
#                     )
#                 else:
#                     logger.info('login successful for {}'.format(email))

#             resp ={
#                     'status':'00',
#                     'token':user.token,

#                     'message':'user loggedin successfully'
#                 }
#             return Response(resp, status=status.HTTP_200_OK)
                
#         return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


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
                        
    