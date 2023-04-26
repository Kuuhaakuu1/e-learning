from django.contrib import admin
from django.urls import path
from login.views import findMagnets, index,home

urlpatterns = [
    path('', index),
    path('index/',findMagnets),
    path('home/',home,name="home")
   
]
