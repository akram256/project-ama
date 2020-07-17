import logging

from django.dispatch import receiver
from djoser.signals import user_registered
from django.conf import settings

from .models import UserProfile

logger = logging.getLogger(__name__)

@receiver(user_registered)
def setup_user_profile(sender, user, **kwargs):
    """ This signal is responsible for creating new user's profile tacking on 
        to djoser's user_registered signal
    """
    UserProfile.objects.create(user=user)
    