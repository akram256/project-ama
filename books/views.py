import logging

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .models import BookModel,BookCategoryModel
from .serializers import BookSerializer,BookCategorySerializer, RatingSerializer
from authentication.models import User
from django.contrib.contenttypes.models import ContentType
from .models import LikeDislike


logger = logging.getLogger(__name__)

class BookView(ListAPIView):
    serializer_class=BookSerializer
    permission_classes=(AllowAny,)
    queryset=BookModel.objects.all()


    def post(self, request):
        post_data = {"name":request.data["name"],"cover_image":request.data["cover_image"],"author":request.data["author"],"price":request.data["price"],"book_url":request.data["book_url"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Book has been  successfully Input"},
                        status=status.HTTP_201_CREATED)


class ChoiceView(ListCreateAPIView):
    """Implements the like and dislike endpoints."""
    
    serializer_class = BookSerializer
    model = None
    vote_type = None
    manager = None

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])

            else:
                likedislike.delete()

        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
        serializer = BookSerializer(obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookCategoryView(ListAPIView):
    serializer_class=BookCategorySerializer
    permission_classes=(AllowAny,)
    queryset=BookCategoryModel.objects.all()


    def post(self, request):
        post_data = {"name":request.data["name"],"cover_image":request.data["cover_image"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Book category  has been  successfully Input"},
                        status=status.HTTP_201_CREATED)


class RatingsView(ListCreateAPIView):
    """
    implements methods to handle rating books
    """
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, id=None):
        """
        method to post a rating for an article
        """
        data = self.serializer_class.update_data(
            request.data.get("book", {}), id)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
                        