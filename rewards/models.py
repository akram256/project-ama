from django.db import models
from utils.models import BaseAbstractModel
from book.models import BookModel

# Create your models here.
class Reward(BaseAbstractModel):
    points=models.DecimalField(max_digits=12, decimal_places=2, null=True, default=Decimal('0.00'))
    book=models.ForeignKey(BookModel,
                                on_delete=models.CASCADE)
    

