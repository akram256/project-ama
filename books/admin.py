from django.contrib import admin
from .models import BookModel,Bookmark,BookCategoryModel,Rating,BookClass, FeedBack
# Register your models here.

admin.site.register(BookModel)
admin.site.register(Bookmark)
admin.site.register(BookCategoryModel)
admin.site.register(Rating)
admin.site.register(BookClass)
admin.site.register(FeedBack)

