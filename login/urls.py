from django.contrib import admin
from django.urls import path
from login.views import index,home,courses

urlpatterns = [
    path('', index),
    path('courses/',courses,name="courses"),
    path('home/',home,name="home")
   
]
