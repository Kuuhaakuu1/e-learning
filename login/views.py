import requests
import pymongo
import string
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import pymongo

def index(request):
    return render(request, 'login.html')

def searchMagnets(keyword):
    client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
    db = client.get_database("Elearning")
    i=0
    # Make a request to the website
    url = 'https://rargb.to/search/?search={}&order=seeders&by=DESC'
    # keyword = input("Enter the keyword: ")
    keywordCollection = db["keywords"]
    keyword = string.capwords(keyword)
    # Define the regular expression pattern to use in the search
    regex_pattern = f".*{keyword}.*"

    # Count the number of documents in the collection that contain the search string
    count = keywordCollection.count_documents({"keyword": {"$regex": regex_pattern}})

    # Check if the count is greater than 0
    if count >=0:
        keywordCollection.insert_one({"keyword": keyword})
        response = requests.get(url.format(keyword))

        ##############################################################################

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the image tags
        courses = soup.find_all('a')

        magnetLinks = db[f"magnets{keyword}"]

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
            #Need to handle the error in a better way    
    # keywordsRead.close()
    # keywordsWrite.close()

def findMagnets(request):
    keyword = 'Java'
    client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
    db = client.get_database("Elearning")
    collectionName = f"magnets{keyword}"

    # collection = db.get_collection(collectionname)
    magnetLinks = db[collectionName].find()
    channel_Id = 'UC8butISFwT-Wl7EV0hUK0BQ'
    live_url = f'https://www.youtube.com/embed/live_stream?channel={channel_Id}'
    # Find all documents in the collection
    # documents = collection.find()
    # query = {'status': 'published'}
    # for document in documents:
    
        # doc = MagnetLinks(document.title, document.magnet)
        # doc.save()
    # d = MagnetLinks.objects.all()
    return render(request, 'index.html',{'data': magnetLinks, 'keyword' : keyword, 'channel_Id' : live_url})
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
    
def courses(request):
    return render(request, 'courses.html')

    
