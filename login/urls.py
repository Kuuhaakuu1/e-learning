from django.contrib import admin
from django.urls import path
from login.views import index,home,courses,register

urlpatterns = [
    path('', index),
    path('courses/',courses,name="courses"),
    path('home/',home,name="home"),
    path('register/',register, name="register"),

   # path('login/', include('djangp.contrib.auth.urls')),
]
