from django.urls import path
from . import views
urlpatterns = [

	path('', views.index),
    path('register', views.process_registration),
    path('login', views.process_login),
    path('welcome', views.welcome),
    path('log_off', views.log_off),
    path('add_book', views.add_book),#adds book to database and favorites it for the logge din user
    path('fav_book/<int:book_id>', views.add_fav), # this one is for adding a book to favorites from the database
    path('book/fav/<int:book_id>', views.edit_fav),
    path('book/<int:book_id>', views.view_book),
    path('unfavorite/<int:book_id>', views.unfav),
    path('delete_book/<int:book_id>', views.delete_book),
    path('process_edit', views.process_edit),
    path('favorite_books/<int:user_id>', views.favorites),
]