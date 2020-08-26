from django.urls import path, include

from store.views import ProductCategoryView, StoreView,ProductRetrieveUpdateView

app_name= 'store'
urlpatterns = [
     path('product/category',ProductCategoryView.as_view(),name='category'),
     path('products',StoreView.as_view(),name='products'),
     path('products/<str:id>',ProductRetrieveUpdateView.as_view(),name='products'),


]