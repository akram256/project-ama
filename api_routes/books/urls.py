from django.urls import path, include

from books.models import LikeDislike, LikeDislikeManager,BookModel
from books.views import ChoiceView,BookView


app_name= 'books'
urlpatterns = [
    path('books',BookView.as_view(),name='books'),

    path('books/<str:id>/like/',
         ChoiceView.as_view(vote_type=LikeDislike.LIKE, model=BookModel,
                            manager=LikeDislikeManager),
         name='book_like'),
    path(
        'books/<str:id>/dislike/',
        ChoiceView.as_view(
            vote_type=LikeDislike.DISLIKE, model=BookModel,
            manager=LikeDislikeManager),
        name='books_dislike'),


]