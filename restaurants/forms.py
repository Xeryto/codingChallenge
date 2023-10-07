import certifi
from django import forms
from pymongo import MongoClient


def return_client():
    CONNECTION_STRING = "mongodb+srv://igoshindanya:632Aa5223@cluster0.fuho1fb.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    return client

client = return_client()

restaurants = list(client['sample_restaurants'].get_collection('restaurants').find().limit(100))

boroughs = ((1, "All"),)
cuisine = ((1, "All"),)
cus = {}
brh = {}
for restaurant in restaurants:
        if (restaurant['borough'] not in brh):
            boroughs = (*boroughs, ((restaurant['borough']), (restaurant['borough'])))
            brh[restaurant['borough']] = 1
        if (restaurant['cuisine'] not in cus):
            cuisine = (*cuisine, ((restaurant['cuisine']), (restaurant['cuisine'])))
            cus[restaurant['cuisine']] = 1

neighborhoods = list(client['sample_restaurants'].get_collection("neighborhoods").find({'has_restaurants': 'true'}))
nghbrhds = ((1, "All"),)
for neighborhood in list(neighborhoods):
        nghbrhds = (*nghbrhds, ((neighborhood['_id']), (neighborhood['name'])))

grade_options = (
    (1, "All"),
    (2, "A"),
    (3, "B or better"),
    (4, "Graded")
)

# creating a form
class FilterForm(forms.Form):
        address_field = forms.ChoiceField(choices=nghbrhds)
        boroughs_field = forms.ChoiceField(choices=boroughs)
        cuisine_field = forms.ChoiceField(choices=cuisine)
        grade_field = forms.ChoiceField(choices=grade_options)

