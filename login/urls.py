from django.contrib import admin
from django.urls import path
from login.views import findMagnets,index,home,courses,register,magnetLists

urlpatterns = [
    path('', index),
    path('courses/',courses,name="courses"),
    path('home/',home,name="home"),
    path('register/',register, name="register"),
    path('magnetLists/',magnetLists, name="magnetLists"),

    path('Java/',findMagnets,name="Java"),
   
]
