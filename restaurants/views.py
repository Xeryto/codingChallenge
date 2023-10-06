from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi


def index(request):
    CONNECTION_STRING = "mongodb+srv://igoshindanya:632Aa5223@cluster0.fuho1fb.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    for collection in client['sample_restaurants'].list_collection_names():
        print(collection)

    return render(request, "restaurants/index.html", {"collections_list": client['sample_restaurants'].list_collection_names()})