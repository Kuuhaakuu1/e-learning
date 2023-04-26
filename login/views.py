from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import pymongo

def index(request):
    return render(request, 'login.html')

def home(request):
    #get post data from request
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        print(username)
        print(password)
        client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
        db = client.get_database("Elearning")
        
        users = db.users
        user = users.find_one({"username": username, "password": password})
        if user is not None:
            return render(request, 'home.html')
        else:
            print("Login failed")
            return render(request, 'home.html')
    else :
        return HttpResponse('Data received')

    
