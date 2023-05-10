import requests
import pymongo
import string
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import MagnetLinks


# Create your views here.
def index(request):
    return render(request, 'login.html')


# def search(request):
#     if request.method == 'POST':
#         keyword = request.POST['keyword']

#         # Connect to the MongoDB database
#         client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test",connectTimeoutMS=60000, 
#                              socketTimeoutMS=60000)
#         db = client.get_database("Elearning")
#         magnet_links = db[f"magnets{keyword}"]
#         count = db["keywords"].count_documents({"keyword": {"$regex": keyword, "$options": "i"}})

#         # if magnet_links.count() == 0:
#         if count == 0:
#             print("No results found in the database")
#             # If no results found in the database, call the searchMagnets function
#             searchMagnets(keyword)
#             magnet_links = db[f"magnets{keyword}"]
#         context = {'data': magnet_links, 'keyword': keyword}
#         return render(request, 'magnets.html', context)

#     return render(request, 'search.html')

    # if request.method == 'POST':
    #     keyword = request.POST['keyword']
    #     magnets = MagnetLinks.objects.filter(title__icontains=keyword)
    #     data = []
    #     for magnet in magnets:
    #         data.append({'title': magnet.title, 'magnet': magnet.magnet})
    #     return render(request, 'search_results.html', {'keyword': keyword, 'data': data})
    # else:
    #     return render(request, 'search.html')

    # if request.method == 'POST':
    #     keyword = request.POST['keyword']

    #     magnet_links = MagnetLinks.objects.filter(title__icontains=keyword)
    #     if not magnet_links:
    #         searchMagnets(keyword)
    #         magnet_links = MagnetLinks.objects.filter(title__icontains=keyword)

    #     context = {'data': magnet_links, 'keyword': keyword}
    #     return render(request, 'magnets.html', context)

    # return render(request, 'search.html')
    
def searchMagnets(request):
    keyword = request.POST.get('keyword')
    client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
    db = client.get_database("Elearning")
    i=0
    # Make a request to the website
    # &order=seeders&by=DESC
    url = 'https://rargb.to/search/?search={}'
    keyword = string.capwords(keyword)

    # Define the regular expression pattern to use in the search
    regex_pattern = f".*{keyword}.*"

    # Count the number of documents in the collection that contain the search string
    count = db["keywords"].count_documents({"keyword": {"$regex": regex_pattern}})
    magnetLinks = db[f"magnets{keyword}"]

    # Check if the count is greater than 0
    if count ==0:
        db["keywords"].insert_one({"keyword": keyword})
        response = requests.get(url.format(keyword))

        ##############################################################################

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the image tags
        courses = soup.find_all('a')


        for course in courses:

            if(str(course).find("/torrent")!=-1):
                href = course['href']
                if(course.text!="  "):
                    next_anchor = course.find_next('a')
                    next_href = next_anchor['href']
                    if(next_href.find("other")!=-1):

                        newurl = 'https://rargb.to/' + str(href)
                        response = requests.get(newurl)

                        # Parse the HTML content
                        soup = BeautifulSoup(response.content, 'html.parser')

                        magnets = soup.find_all('a')
                        
                        for magnet in magnets:
                            if(str(magnet).find("magnet:")!=-1):
                                href = magnet['href']
                                magnetLinks.insert_one({"name":course.text, "magnet": str(href)})
                                i+=1
        if(i==0):
            magnetLinks.drop()

    # Get the data from the database
    data = []
    for el in magnetLinks.find():
        data.append(el)

    # Render the HTML template with the data
    context = {'keyword': keyword, 'data': data}
    return render(request, 'magnetLists.html', context)



# def searchMagnets(keyword):
#     client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
#     db = client.get_database("Elearning")
#     i=0
#     # Make a request to the website
#     url = 'https://rargb.to/search/?search={}&order=seeders&by=DESC'
#     # keyword = input("Enter the keyword: ")
#     keywordCollection = db["keywords"]
#     keyword = string.capwords(keyword)
#     # Define the regular expression pattern to use in the search
#     regex_pattern = f".*{keyword}.*"

#     # Count the number of documents in the collection that contain the search string
#     count = keywordCollection.count_documents({"keyword": {"$regex": regex_pattern}})

#     # Check if the count is greater than 0
#     if count >=0:
#         keywordCollection.insert_one({"keyword": keyword})
#         response = requests.get(url.format(keyword))

#         ##############################################################################

#         # Parse the HTML content
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Find all the image tags
#         courses = soup.find_all('a')

#         magnetLinks = db[f"magnets{keyword}"]

#         for course in courses:

#             if(str(course).find("/torrent")!=-1):
#                 href = course['href']
#                 if(course.text!="  "):
#                     next_anchor = course.find_next('a')
#                     next_href = next_anchor['href']
#                     if(next_href.find("other")!=-1):

#                         newurl = 'https://rargb.to/' + str(href)
#                         response = requests.get(newurl)

#                         # Parse the HTML content
#                         soup = BeautifulSoup(response.content, 'html.parser')

#                         magnets = soup.find_all('a')
                        
#                         for magnet in magnets:
#                             if(str(magnet).find("magnet:")!=-1):
#                                 href = magnet['href']
#                                 magnetLinks.insert_one({"name":course.text, "magnet": str(href)})
#                                 i+=1
#         if(i==0):
#             magnetLinks.drop()
#             #Need to handle the error in a better way    
#     # keywordsRead.close()
#     # keywordsWrite.close()

def findMagnets(request):
    keyword = 'Java'
    client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
    db = client.get_database("Elearning")
    collectionName = f"magnets{keyword}"

    # collection = db.get_collection(collectionname)
    magnetLinks = db[collectionName].find()
    # channel_Id = 'UC8butISFwT-Wl7EV0hUK0BQ'
    # live_url = f'https://www.youtube.com/embed/live_stream?channel={channel_Id}'
    
    # Find all documents in the collection
    # documents = collection.find()
    # query = {'status': 'published'}
    # for document in documents:
    
        # doc = MagnetLinks(document.title, document.magnet)
        # doc.save()
    # d = MagnetLinks.objects.all()
    # , 'channel_Id' : live_url
    return render(request, 'magnetLists.html',{'data': magnetLinks, 'keyword' : keyword})

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
       # hashed_password = make_password(password)

        
        # insert user data into database
        user_data = {
            'username': username,
            'password': password,
            'email': email,
            'phone': phone,
            'role': role
        }
        users.insert_one(user_data)
        show_success = True  # add a variable to track whether to show the alert or not
        return render(request, 'home.html', {'show_success': show_success})
        
    return render(request, 'register.html')

def magnetLists(request):
    return render(request, 'magnetLists.html')