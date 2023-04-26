import requests
import string
import os
import pymongo
from bs4 import BeautifulSoup
from django.shortcuts import render

from login.models import MagnetLinks


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
    # keywordsRead = open("keywords.txt", "r")
    # keywordsWrite = open("keywords.txt", "a")
    # if(keywordCollection.find(keyword)==-1):
        keywordCollection.insert_one({"keyword": keyword})
        #insert magnet links in database and read from them

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
                                # text_file.write(course.text + '\n')
                                # text_file2.write(str(href) + '\n')
                                i+=1
        # text_file.close()
        # text_file2.close()
        if(i==0):
            # print("No magnets found, Sorry!")
            magnetLinks.drop()
            #Need to handle the error in a better way    
    # keywordsRead.close()
    # keywordsWrite.close()

###################################### test function ######################################

def findMagnets(request):
    keyword = 'Java'
    client = pymongo.MongoClient("mongodb+srv://admin:S0uf14n3_0m4R_$44d@elearning.i6x9053.mongodb.net/test")
    db = client.get_database("Elearning")
    collectionname = f"magnets{keyword}"
    collection = db.get_collection(collectionname)

    # Find all documents in the collection
    documents = collection.find()
    for document in documents:
        doc = MagnetLinks(document.title, document.magnet)
        doc.save()
    d = MagnetLinks.objects.all()
    return render(request, 'index.html',{'data': d})
###################################### test function ######################################