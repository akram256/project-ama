from rest_framework import serializers
from .models import ProductCategory, Store

class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializer for Product category"""
    class Meta:
        model=ProductCategory
        fields=('__all__')

class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store"""
    class Meta:
        model=Store
        fields=('id','product','price','specifications','image','variation','origin','category','product_category','created_at')
