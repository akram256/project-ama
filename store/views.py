import logging

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .models import ProductCategory, Store
from .serializers import ProductCategorySerializer,StoreSerializer

logger = logging.getLogger(__name__)

# Create your views here.

class ProductCategoryView(ListAPIView):
    """View for Product Category"""
    serializer_class= ProductCategorySerializer
    permission_classes= (AllowAny,)
    queryset= ProductCategory.objects.all()

class StoreView(ListAPIView):
    serializer_class=StoreSerializer
    permission_classes=(AllowAny,)
    queryset = Store.objects.all()

class ProductRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    """Handles retriving a single product"""

    permission_classes =(AllowAny,)
    serializer_class = StoreSerializer
    lookup_field = 'id'
    queryset = Store.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))