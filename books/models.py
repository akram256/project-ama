import uuid
import base64
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from utils.models import BaseAbstractModel
from decimal import Decimal
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from authentication.models import User


# class BookCategoryModel(BaseAbstractModel):
#     user = models.OneToOneField(User,
#                                 unique=True,
#                                 verbose_name=_('user'),
#                                 on_delete=models.CASCADE)
#     name = models.CharField(max_length=300, blank=True, null=True)
#     cover_image= models.CharField(max_length=300, blank=True, null=True)
#     book_url = models.CharField(max_length=300, blank=True, null=True)
#     price = models.CharField(max_length=300, blank=True, null=True)
#     author = models.CharField(max_length=300, blank=True, null=True)
    # category = models.CharField(max_length=300, blank=True, null=True)


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


class BookModel(BaseAbstractModel):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True, null=True)
    cover_image= models.CharField(max_length=300, blank=True, null=True)
    book_url = models.CharField(max_length=300, blank=True, null=True)
    price = models.CharField(max_length=300, blank=True, null=True)
    author = models.CharField(max_length=300, blank=True, null=True)
    votes = GenericRelation(LikeDislike, related_name='articles')
    # category = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name
    


