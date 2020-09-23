import re
import logging

from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import User,Age_Category,UserProfile
# School,UserProfile,




logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','first_name','last_name','email')
    
def swap(value,new):
    if value :
        return value
    else:
        return new


class RegistrationSerializer(serializers.Serializer):
    """Serializer registration requests and create a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )
    confirmed_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name",'school_name','school_address','role',
                  "password", "confirmed_password",]

    def validate(self, data):
        """Validate data before it gets saved."""

        confirmed_password = data.get("confirmed_password")
        try:
            validate_password(data["password"])
        except ValidationError as identifier:
            raise serializers.ValidationError({
                "password": str(identifier).replace(
                    "["", "").replace(""]", "")})

        if not self.do_passwords_match(data["password"], confirmed_password):
            raise serializers.ValidationError({
                "passwords": ("Passwords do not match")
            })

        return data

    def create(self, validated_data):
        """Create a user."""
        del validated_data["confirmed_password"]
        return User.objects.create_user(**validated_data)

    def do_passwords_match(self, password1, password2):
        """Check if passwords match."""
        return password1 == password2


class GenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "school_name",]



class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)
    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate_phone_no(self, valuUsere):
        if not value:
            raise serializers.ValidationError(
                'An phone_no is required to log in.'
            )
        return value 
    def validate_password(self, value):
        if value is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        return value

# class UserProfileSerializer(serializers.Serializer):
#     class Meta:
#         model=UserProfile
#         fields=('__all__')

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Age_Category
        fields=('id','age_category')

class UpdateProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()

    def update(self, instance, validated_data):
        user_data=validated_data['user']
        print(user_data)
        instance.user.email = swap(user_data.get('email'), instance.user.email)
        instance.user.first_name = swap(user_data.get('first_name'), instance.user.first_name)
        instance.user.last_name = swap(user_data.get('last_name'), instance.user.last_name)
        instance.image= swap(validated_data.get('image'),instance.image)
        instance.address= swap(validated_data.get('address'),instance.address)
        instance.city= swap(validated_data.get('city'),instance.city)
        instance.country= swap(validated_data.get('country'),instance.country)
        instance.user.save()
        instance.save()
        return instance

    class Meta:
        model=UserProfile
        fields=['id','user', 'address', 'city','country','image']


class SubcriptionSerializer(serializers.Serializer):
    amount = serializers.CharField(required=True, allow_blank=True, max_length=100)
    email = serializers.CharField(required=True, allow_blank=True, max_length=100)

class VerifySubscriptionSerializer(serializers.Serializer):
    reference = serializers.CharField()

