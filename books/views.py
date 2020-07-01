import logging

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated

from .models import BookModel
from .serializers import BookSerializer
from authentication.models import User


logger = logging.getLogger(__name__)

class BookView(ListAPIView):
    serializer_class=BookSerializer
    permission_classes=(AllowAny,)
    queryset=BookModel.objects.all()


    def post(self, request):
        post_data = {"name":request.data["name"],"author":request.data["author"],"price":request.data["price"],"book_url":request.data["book_url"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Book has been  successfully Input"},
                        status=status.HTTP_201_CREATED)
