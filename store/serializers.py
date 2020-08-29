from rest_framework import serializers
from .models import ProductCategory, Store,Cart

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

class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart"""

    product_name = serializers.ReadOnlyField(source='product.product')
    price = serializers.ReadOnlyField(source='product.price')
    specifications = serializers.ReadOnlyField(source='product.specifications')
    image=serializers.ReadOnlyField(source='product.image')
    variation = serializers.ReadOnlyField(source='product.variation')
    origin = serializers.ReadOnlyField(source='product.origin')
    created_at=serializers.ReadOnlyField(source='product.created_at')
    
    class Meta:
        model = Cart
        fields=("id","product_name",'price','specifications','image','variation','origin',"created_at")