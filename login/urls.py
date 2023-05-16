from django.contrib import admin
from django.urls import path
from login.views import index,home,courses,register,searchMagnets,teachers,logout,students

urlpatterns = [
    path('', index),
    path('courses/',courses,name="courses"),
    path('home/',home,name="home"),
    path('register/',register, name="register"),
    path('study/', searchMagnets, name='study'),
    path('magnets/<str:keyword>/', searchMagnets, name='magnets'),
    path('home/teacher/', teachers, name='teacher'),
    path('home/students/', students, name='student'),
    path('logout/', logout, name='logout'),
   
]
