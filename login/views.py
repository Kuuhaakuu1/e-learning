import requests
import pymongo
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password



# Create your views here.
def index(request):
    return render(request, 'login.html')

def home(request):
    # get post data from request
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
        db = client.get_database("Elearning")
        
        users = db.users
        user = users.find_one({"username": username, "password": password})
        if user is not None:
            return render(request, 'home.html')
        else:
            show_alert = True  # add a variable to track whether to show the alert or not
            return render(request, 'login.html', {'show_alert': show_alert})
    
    else:
        return render(request, 'login.html')   

def courses(request):
    return render(request, 'courses.html')


# signup hh
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        
        # validate form data
        if not username or not password or not email or not phone or not role:
            messages.error(request, 'Please fill all required fields')
            return render(request, 'register.html')
        
        # check if user already exists
        client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
        db = client.get_database('Elearning')
        users = db.users
        if users.find_one({'username': username}):
            show_message = True  # add a variable to track whether to show the alert or not
            return render(request, 'register.html', {'show_message': show_message})
        
        # hash password
        hashed_password = make_password(password)
        
        # insert user data into database
        user_data = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'phone': phone,
            'role': role
        }
        users.insert_one(user_data)
        show_success = True  # add a variable to track whether to show the alert or not
        return render(request, 'home.html', {'show_success': show_success})
        
    return render(request, 'register.html')