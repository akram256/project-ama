import logging
from rest_framework import serializers
from .models import BookModel


logger = logging.getLogger(__name__)

class BookSerializer(serializers.Serializer):
    """This is a serializer of books model"""
    class Meta:
        model=BookModel
        fields=['__all__']

