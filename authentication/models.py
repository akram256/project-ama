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
    ROLES = (
        ('SCHOOL', 'SCHOOL'),
        ('USER', 'USER')
    )
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=255, blank=True, null=True, choices=ROLES)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    school_address= models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True,unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_new_user=models.BooleanField(default=False)

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

class UserProfile(BaseAbstractModel):
    """User Profile Model"""

    user = models.OneToOneField(to='User', on_delete=models.CASCADE)
    image=  models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.first_name
    
    @property
    def email(self):
        return self.user.email

class Age_Category(BaseAbstractModel):
    """"Age category Model"""

    age_category=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.age_category

 