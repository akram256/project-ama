from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from utils.models import BaseAbstractModel
from .managers import UserManager
import uuid
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from decimal import Decimal

class User(AbstractBaseUser, PermissionsMixin, BaseAbstractModel):
    """This is a user model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True,unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name',]
    objects = UserManager()

    def __str__(self):
        if self.first_name:
            return "{}".format(self.first_name)
        return "{}".format(self.email)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=365)

        token = jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class School(AbstractBaseUser):
    """This is model for a school"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    school_email = models.CharField(max_length=255, blank=True, null=True)
    school_address= models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'school_email'
    REQUIRED_FIELDS = ['school_name',]
    objects = UserManager()

    def __str__(self):
        if self.school_name:
            return "{}".format(self.school_name)
        return "{}".format(self.school_email)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=365)

        token = jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
 