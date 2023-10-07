from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from django import forms
from .forms import *
from bson import ObjectId

def return_client():
    CONNECTION_STRING = "mongodb+srv://igoshindanya:632Aa5223@cluster0.fuho1fb.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    neighborhoods = client['sample_restaurants'].get_collection('neighborhoods')
    neighborhoods.update_many({'has_restaurants': {'$exists' : 'false'}}, {"$set": {"has_restaurants": 'false'}})
    neighborhoods.update_many({}, {"$set": {"has_restaurants": 'false'}})
    restaurants = list(client['sample_restaurants'].get_collection('restaurants').find().limit(100))
    points = []
    for restaurant in restaurants:
        if restaurant['address']['coord'] != []:
            points+=[Point(restaurant['address']['coord'])]

    for neighborhood in list(neighborhoods.find()):
        coords = neighborhood['geometry']['coordinates'][0]
        if (len(coords) == 1):
            coords = coords[0]
        polygon = Polygon(coords)
        for point in points:
            if polygon.contains(point):
                neighborhoods.update_one({'_id': neighborhood['_id']}, {'$set': {'has_restaurants': 'true'}})
                break
    return client

def index(request):
    client = return_client()

    restaurants = client['sample_restaurants'].get_collection('restaurants').find().limit(100)

    if request.GET:
        neighborhood = request.GET['address_field']
        cuisine = request.GET['cuisine_field']
        borough = request.GET['boroughs_field']
        grade = request.GET['grade_field']
        name = request.GET['name']

        if cuisine != "1" or borough != "1" or name != None:
            if borough != "1" and cuisine != "1" and name != None:
                restaurants = client['sample_restaurants'].get_collection('restaurants').find({
                    'cuisine': cuisine, "borough": borough, 'name': {'$regex': name, '$options': 'i'}}).limit(100)
            elif borough != "1" and name != None:
                restaurants = client['sample_restaurants'].get_collection('restaurants').find(
                    {'name': {'$regex': name, '$options': 'i'}, 'borough': borough}).limit(100)
            elif cuisine != "1" and name != None:
                restaurants = client['sample_restaurants'].get_collection('restaurants').find(
                    {'cuisine': cuisine, 'name': {'$regex': name, '$options': 'i'}}).limit(100)
            elif cuisine != "1" and borough != "1":
                restaurants = client['sample_restaurants'].get_collection('restaurants').find({
                    'cuisine': cuisine, "borough": borough}).limit(100)
            elif name != None:
                restaurants = client['sample_restaurants'].get_collection('restaurants').find(
                    {'name': {'$regex': name, '$options': 'i'}}).limit(100)
            elif cuisine != "1":
                restaurants = client['sample_restaurants'].get_collection('restaurants').find(
                    {'cuisine': cuisine}).limit(100)
            else:
                restaurants = client['sample_restaurants'].get_collection('restaurants').find(
                    {'borough': borough}).limit(100)

        if neighborhood != "1" or grade != "1":
            if neighborhood != "1":
                neighborhood = ObjectId(neighborhood)
                coords = client['sample_restaurants'].get_collection("neighborhoods").find_one({'_id': neighborhood})[
                    'geometry']['coordinates'][0]
                if (len(coords) == 1):
                    coords = coords[0]
                filtered_restaurants = []
                for restaurant in list(restaurants):
                    point = Point(restaurant['address']['coord'])
                    polygon = Polygon(coords)
                    if polygon.contains(point):
                        if grade != "1":
                            restaurant['grade'] = list(filter(lambda x: x['date'], list(restaurant['grades'])))[0]['grade']
                        filtered_restaurants += [restaurant]

                restaurants = filtered_restaurants
                if grade != "1":
                    if grade == "2":
                        restaurants = list(filter(lambda x: x['grade'] == "A", restaurants))
                    elif grade == "3":
                        restaurants = list(filter(lambda x: x['grade'] in ["A", "B"], restaurants))
                    else:
                        restaurants = list(filter(lambda x: x['grade'] in ["A", "B", "C"], restaurants))
            else:
                restaurants = list(restaurants)
                for restaurant in restaurants:
                    restaurant['grade'] = list(filter(lambda x: x['date'], list(restaurant['grades'])))[0]['grade']
                if grade == "2":
                    restaurants = list(filter(lambda x: x['grade'] == "A", restaurants))
                elif grade == "3":
                    restaurants = list(filter(lambda x: x['grade'] in ["A", "B"], restaurants))
                else:
                    restaurants = list(filter(lambda x: x['grade'] in ["A", "B", "C"], restaurants))
        else: restaurants = list(restaurants)
    else:
        restaurants = list(restaurants)

    for restaurant in restaurants:
        restaurant['grade'] = list(filter(lambda x: x['date'], list(restaurant['grades'])))[0]['grade']
        restaurant['string_address'] = restaurant['address']['building']+' '+restaurant['address']['street']+", "+restaurant['address']['zipcode']

    context = {}
    context['restaurants'] = restaurants
    context['form'] = FilterForm()



    return render(request, "restaurants/index.html", context)

def details(request, restaurant_id):
    client = return_client()
    restaurant = client['sample_restaurants'].get_collection('restaurants').find_one({'restaurant_id': str(restaurant_id)})
    point = Point(restaurant['address']['coord'])
    restaurant['grade'] = list(filter(lambda x: x['date'], list(restaurant['grades'])))[0]['grade']
    restaurant['string_address'] = restaurant['address']['building'] + ' ' + restaurant['address']['street'] + ", " + \
                            restaurant['address']['zipcode']

    neighborhoods = client['sample_restaurants'].get_collection('neighborhoods')
    for neighborhood in list(neighborhoods.find()):
        coords = neighborhood['geometry']['coordinates'][0]
        if (len(coords) == 1):
            coords = coords[0]
        polygon = Polygon(coords)
        if polygon.contains(point):
            restaurant['neighborhood'] = neighborhood['name']
            break


    context = {}
    context['restaurant'] = restaurant

    return render(request, 'restaurants/details.html', context)

def grades(request, id):
    print("yay")

def add_grade(request, id):
    print("yay")