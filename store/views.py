import logging
from decimal import Decimal

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .models import ProductCategory, Store,Cart
from .serializers import ProductCategorySerializer,StoreSerializer,CartSerializer
from .filters import StoreFilter

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
    filter_class = StoreFilter

class ProductRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    """Handles retriving a single product"""

    permission_classes =(AllowAny,)
    serializer_class = StoreSerializer
    lookup_field = 'id'
    queryset = Store.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))
            

class CartView(ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    # queryset = Cart.objects.all()


    def create(self, request, *args, **kwargs):
        product = get_object_or_404(Store, id=self.kwargs.get('id'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, product):
        serializer.save(user=self.request.user,product=product)

class CartProducts(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
   

    def get_queryset(self,request):
        products = Cart.objects.filter(user=request.user) 

        products_amount=products.values("product__price")
        print(products_amount)
        total_amount = lambda x : sum([float(data['product__price']) for data in x])

        return products, total_amount(products_amount)

    def get(self,request):
        data = self.get_queryset(request)
        serializer = self.serializer_class(data[0], many=True)
        if data:
            payload={'data':serializer.data,
                    'Total Price':data[1],

                    }
            return Response(payload, status=status.HTTP_200_OK) 
        else:
            return Response({'message': 'Requested resources that does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


