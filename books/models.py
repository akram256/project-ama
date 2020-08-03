import uuid
import base64
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from utils.models import BaseAbstractModel
from authentication.models import User


class BookCategoryModel(BaseAbstractModel):
    """Model of book categories of interest"""
    name = models.CharField(max_length=300, blank=True, null=True)
    cover_image= models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name


class LikeDislikeManager(models.Manager):
    # Gets all the votes greater than 0. In this case they're likes.
    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    # Gets all the votes less than 0. In this case they're dislikes.
    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)


class LikeDislike(BaseAbstractModel):
    """Likes and Dislikes model."""
    LIKE = 1
    DISLIKE = -1

    VOTES = ((DISLIKE, 'Dislike'), (LIKE, 'Like'))

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

class BookClass(BaseAbstractModel):
    """Model for book categories"""

    name=models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name


class BookModel(BaseAbstractModel):
    """
        Model for books
    """
    name = models.CharField(max_length=300, blank=True, null=True)
    cover_image=  models.ImageField(upload_to='books/', null=True)
    book_url = models.CharField(max_length=300, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    author = models.CharField(max_length=300, blank=True, null=True)
    votes = GenericRelation(LikeDislike, related_name='books')
    user_rates = models.CharField(max_length=10, default=0)
    is_liked=models.BooleanField(default=False)
    is_rated=models.BooleanField(default=False)
    is_bookmarked=models.BooleanField(default=False)
    book_category = models.ForeignKey(BookClass,
                                on_delete=models.CASCADE)
    # category = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def category(self):
        return self.book_category.name
    
    @property
    def average_rating(self):
        """
        method to calculate the average rating of the article.
        """
        ratings = self.scores.all().aggregate(score=Avg("score"))
        return float('%.2f' % (ratings["score"] if ratings['score'] else 0))


class Rating(models.Model):
    """
        Model for rating an book
    """
    book = models.ForeignKey(BookModel, related_name="scores",
                                on_delete=models.CASCADE)
    rated_on = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)


    class Meta:
        ordering = ["-score"]
    
    @property
    def is_rated(self):
        return self.book.is_rated

class Bookmark(BaseAbstractModel):
    """
        Model for bookmarking
    """
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.book


