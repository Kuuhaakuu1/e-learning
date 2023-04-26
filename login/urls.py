from django.contrib import admin
from django.urls import path
from login.views import index
from login.views import findMagnets

urlpatterns = [
    path('', index),
    path('index/',findMagnets),
]
