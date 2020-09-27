from decimal import Decimal

from django.db import models
from django.conf import settings
from authentication.models import User

from utils.models import BaseAbstractModel


# Create your models here.
class ProductCategory(BaseAbstractModel):

    """Product category"""

    name=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Store(BaseAbstractModel):
    """Model to sell Store Commodities"""

    product=models.CharField(max_length=255, blank=True, null=True)
    price=models.DecimalField(max_digits=12, decimal_places=2, null=True, default=Decimal('0.00'))
    specifications=models.CharField(max_length=255, blank=True, null=True)
    image=models.CharField(max_length=255, blank=True, null=True)
    variation= models.DecimalField(max_digits=12, decimal_places=2, null=True, default=Decimal('0.00'))
    origin=models.CharField(max_length=255, blank=True, null=True)
    category= models.ForeignKey(ProductCategory,
                                on_delete=models.CASCADE)

    
    def __str__(self):
        return self.product

    @property
    def product_category(self):
        return self.category.name


class Cart(BaseAbstractModel):

   
    product=models.ForeignKey(Store,
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    counter=models.IntegerField(blank=True, null=True, default=0)
    
    def __str__(self):
        return str(self.product)


