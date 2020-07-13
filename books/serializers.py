import logging
from rest_framework import serializers
from .models import BookModel


logger = logging.getLogger(__name__)

class BookSerializer(serializers.Serializer):
    """This is a serializer of books model"""
    class Meta:
        model=BookModel
        fields=['name','cover_image','book_url','price','author','likes','dislikes']

    # Gets all the books likes
    def get_likes(self, instance):
        return instance.votes.likes().count()

    # # Gets all the books dislikes
    def get_dislikes(self, instance):
        return instance.votes.dislikes().count()

