from django.contrib import admin
from .models import BookModel,Bookmark
# Register your models here.

admin.site.register(BookModel)
admin.site.register(Bookmark)
