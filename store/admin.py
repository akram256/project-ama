from django.contrib import admin
 
from .models import Store, ProductCategory

# Register your models here.
admin.site.register(Store)
admin.site.register(ProductCategory)