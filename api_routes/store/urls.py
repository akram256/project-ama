from django.urls import path, include

from store.views import ProductCategoryView, StoreView,ProductRetrieveUpdateView,CartView,CartProducts

app_name= 'store'
urlpatterns = [
     path('product/category',ProductCategoryView.as_view(),name='category'),
     path('products',StoreView.as_view(),name='products'),
     path('products/<str:id>',ProductRetrieveUpdateView.as_view(),name='products'),
     path('cart/<str:id>',CartView.as_view(),name='cart'),
     path('buy/products',CartProducts.as_view(),name='all-cart-products'),



]