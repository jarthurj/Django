from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.process_registration),
    path('login', views.process_login),
    path('success', views.success),
    path('log_out', views.log_out)
]
