import base64
from django.db import models
from accounts.models import User, UserProfile
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from utils.models import BaseAbstractModel
from decimal import Decimal
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class AudioModel(BaseAbstractModel):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True, null=True)
    cover_image= models.CharField(max_length=300, blank=True, null=True)
    audio_url = models.CharField(max_length=300, blank=True, null=True)
