from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.process_registration),
    path('login', views.process_login),
    path('wall', views.wall),
    path('log_off', views.log_off),
    path('post_message', views.post_message),
    path('post_comment/<int:message_id>', views.post_comment),
    path('delete/message/<int:message_id>', views.delete_message),
    path('delete/comment/<int:comment_id>', views.delete_comment),

]
