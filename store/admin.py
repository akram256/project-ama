from django.contrib import admin
 
from .models import Store, ProductCategory,Cart

# Register your models here.
admin.site.register(Store)
admin.site.register(ProductCategory)
admin.site.register(Cart)