import logging
from rest_framework import serializers
from .models import BookModel,BookCategoryModel,Rating, Bookmark


logger = logging.getLogger(__name__)

class BookSerializer(serializers.ModelSerializer):
    """This is a serializer of books model"""
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    class Meta:
        model=BookModel
        fields=['id','name','cover_image','book_url','price','author','likes','dislikes', 'is_liked','is_rated','is_bookmarked','average_rating',
            'user_rates',]

    # Gets all the books likes

    def get_likes(self, instance):
        return instance.votes.likes().count()

    # # Gets all the books dislikes
    def get_dislikes(self, instance):
        return instance.votes.dislikes().count()

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=BookCategoryModel
        fields= ('__all__')


class RatingSerializer(serializers.ModelSerializer):
    """
    class holding logic for article rating
    """
    book = serializers.PrimaryKeyRelatedField(
        queryset=BookModel.objects.all())
    rated_on = serializers.DateTimeField(read_only=True)
    score = serializers.DecimalField(required=True, max_digits=5,
                                     decimal_places=2)

    @staticmethod
    def update_data(data, id):
        """
        method to update the book with a rating
        """
        try:
            book = BookModel.objects.get(id__exact=id)
        except BookModel.DoesNotExist:
            raise serializers.ValidationError("Book is not found.")

        score = data.get("score", 0)
        if score > 5 or score < 0:
            raise serializers.ValidationError({
                "error": ["Score value must not go "
                          "below `0` and not go beyond `5`"]
            })
        data.update({"book": book.pk})   
        print(data)
        return data

    def create(self, validated_data):
        """
        method to create and save a rating for
        """
    
        book = validated_data.get("book", None)
        score = validated_data.get("score", 0)

        try:
            rating = Rating.objects.get(
                book__id=book.id)
        except Rating.DoesNotExist:
            return Rating.objects.create(**validated_data)
        rating.score = score
        book.is_rated=True
        rating.save()
        book.save()
        return rating

    class Meta:
        """
        class behaviours
        """
        model = Rating
        fields = ("score", "rated_on", "book","is_rated")


class BookmarkSerializer(serializers.ModelSerializer):
    Reader = serializers.ReadOnlyField(source='user.email')
    # user = serializers.ReadOnlyField(source='user')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    book_name = serializers.ReadOnlyField(source='book.name')
    book_url = serializers.ReadOnlyField(source='book.book_url')
    price = serializers.ReadOnlyField(source='book.price')
    book__id=serializers.ReadOnlyField(source='book.id')
    rating = serializers.ReadOnlyField(source='book.average_rating')
    is_bookmarked = serializers.ReadOnlyField(source='book.is_bookmarked')
    # likes = serializers.ReadOnlyField(source='book.votes.likes')
    class Meta:
        model = Bookmark
        fields = ('Reader','first_name','book__id','book_name','book_url','price','rating','is_bookmarked')