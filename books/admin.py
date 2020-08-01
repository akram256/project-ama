from django.contrib import admin
from .models import BookModel,Bookmark,BookCategoryModel
# Register your models here.

admin.site.register(BookModel)
admin.site.register(Bookmark)
admin.site.register(BookCategoryModel)

