from django.contrib import admin
from django.urls import path
from login.views import index,home,courses,register,searchMagnets,teachers,logout,students,edit

urlpatterns = [
    path('', index),
    path('courses/',courses,name="courses"),
    path('home/',home,name="home"),
    path('register/',register, name="register"),
    path('streaming/',streaming, name="streaming"),

    # path('magnetLists/',magnetLists, name="magnetLists"),

    # path('Java/',findMagnets,name="Java"),
    # path('test/<str:param>/',findMagnets,name="courseMagnets"),
    path('study/', searchMagnets, name='study'),
    path('magnets/<str:keyword>/', searchMagnets, name='magnets'),
    path('home/edit/<slug:uid>/', edit, name='edit'),
    path('home/teacher/', teachers, name='teacher'),
    path('home/students/', students, name='student'),
    path('logout/', logout, name='logout'),
   
]
