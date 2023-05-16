from django.contrib import admin
from django.urls import path
from login.views import index,home,courses,register,searchMagnets,streaming

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
   
]
