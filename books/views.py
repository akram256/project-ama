import logging

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView,ListAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .models import BookModel,BookCategoryModel,Bookmark, BookClass
from .serializers import BookSerializer,BookCategorySerializer,BookClassSerializer, RatingSerializer,BookmarkSerializer
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

class BookClassView(ListAPIView):
    """"implements categories of books"""

    serializer_class=BookClassSerializer
    permission_classes=(AllowAny,)
    queryset=BookClass.objects.all()

    def post(self, request):
        post_data = {"name":request.data["name"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Book Category has been  successfully Input"},
                        status=status.HTTP_201_CREATED)

class ChoiceView(ListCreateAPIView):
    """Implements the like and dislike endpoints."""
    
    serializer_class = BookSerializer
    model = None
    vote_type = None
    manager = None

    def post(self, request, id):
        obj = self.model.objects.get(id=id)

        # is_liked=obj.is_liked
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
                obj.is_liked=False
                obj.save()

        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            obj.is_liked=True
            obj.save()
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
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookmarkView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()


    def create(self, request, *args, **kwargs):
        book = get_object_or_404(BookModel, id=self.kwargs.get('id'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Bookmark.objects.filter(
            book=book.id, user=request.user.id)
        if instance:
            return Response({"message": "book already bookmarked"},
                            status=status.HTTP_200_OK)

        self.perform_create(serializer,book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, book):
        book.is_bookmarked=True
        book.save()
        serializer.save(user=self.request.user, book=book)


class UnBookmarkView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer
    lookup_field = 'id'
    queryset = Bookmark.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = Bookmark.objects.filter(
            user_id=request.user.id, book=self.kwargs['id'])
        if not instance:
            return Response({"message": "book not found"},
                            status=status.HTTP_404_NOT_FOUND)
        book=BookModel.objects.get(id=self.kwargs['id'])
        book.is_bookmarked=False
        book.save()
        self.perform_destroy(instance)
        return Response({"message": "Book successfully unbookmarked"},
                        status=status.HTTP_200_OK)


class ListBookmarksView(ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Bookmark.objects.all()

    def get(self, request, *args, **kwargs):
        bookmarks = self.queryset.filter(
            user_id=request.user)
        serializer = self.serializer_class(bookmarks, many=True)
        return Response({'data':serializer.data, },status=status.HTTP_200_OK)
                        