from django.contrib import admin
from django.urls import path
from login.views import index,home

urlpatterns = [
    path('', index),
    path('home/',home,name="home")
   
]
