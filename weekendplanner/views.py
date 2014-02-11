from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template.loader import *
from django.utils.html import escape
import requests, facebook
from facebook import FacebookAPI, GraphAPI, FacebookClientError
from weekendplanner.app.models import *
from string import replace
import json, random

APP_KEY = "613925892012742"
APP_SECRET = "e3c87fa61e6d9b587a63268623049ce6"
FACEBOOK_REDIRECT = "http://www.planmyny.com/facebook_login"

NY_TIMES_API_KEY = "ac8e622d58c2753ea21809d358c146cb:9:68789349"
GOOGLE_API_KEY = "AIzaSyDhoZ2Yyii_wvZaWSqUu4BilsVAfJHZIzk"

GEOCODING_STRING_COLUMBIA = "http://maps.googleapis.com/maps/api/geocode/json?address=2920+Broadway,+New+York,+NY&sensor=false"
GEOCODING_BASE_STRING = "http://maps.googleapis.com/maps/api/geocode/json?address="

COLUMBIA_LAT = "40.807001"
COLUMBIA_LONG = "-73.9640299"

GOOGLE_PLACES_BASE_STRING = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
GOOGLE_DETAILS_BASE_STRING = "https://maps.googleapis.com/maps/api/place/details/json?reference="

NEW_YORK_TIMES_BASE_STRING = "http://api.nytimes.com/svc/events/v2/listings.json?api-key=" + NY_TIMES_API_KEY

GOOGLE_MAPS_BASE_STRING = "http://maps.googleapis.com/maps/api/staticmap?"
 
def search(request):
    url = "https://api.github.com/search/repositories?q=Space%20Invaders%20HTML5+language:JavaScript"
    response = requests.get(url).json()
    return render_to_response('home.html', {})

def home(request):
    if "facebook_id" in request.session:
        return redirect("/profile")
    else:
        f = FacebookAPI(APP_KEY, APP_SECRET, FACEBOOK_REDIRECT)
        auth_url = f.get_auth_url(scope=['create_event', 'user_photos', 'user_location'])
        c = {}
        c['fb_url'] = auth_url
        response = requests.get(GEOCODING_STRING_COLUMBIA).json()
        c['location'] = response['results'][0]['geometry']['location']
        c['places'] = get_orbit_data()
        c['api_key'] = GOOGLE_API_KEY
        return render_to_response('index.html', c)
    
def facebook_login(request):
    code = request.GET.get('code')
    f = FacebookAPI(APP_KEY, APP_SECRET, FACEBOOK_REDIRECT)
    access_token = f.get_access_token(code)
    final_access_token = access_token['access_token']
    request.session['access_token'] = final_access_token
    graph = GraphAPI(final_access_token)
    try:
        me = graph.get('me')
        request.session['facebook_id'] = me['id']
        request.session['first_name'] = me['first_name']
        request.session['last_name'] = me['last_name']
        if (len(FacebookUser.objects.filter(facebook_id=me['id'])) == 0):
            f = FacebookUser.create(me['id'],me['first_name'],me['last_name'])
            f.save()
        return redirect('/profile/')
    except FacebookClientError:
        return HttpResponse("Sorry, something went wrong.")

def profile(request):
    c={}
    if 'facebook_id' in request.session:
        c['facebook_id'] = request.session['facebook_id']
        c['first_name'] = request.session['first_name']
        c['last_name'] = request.session['last_name']
        c['events'] = profile_upcoming_events()
        facebook_user = FacebookUser.objects.filter(facebook_id=request.session['facebook_id'])[0]
        trips = Trip.objects.filter(user=facebook_user)
        if (len(trips) > 0):
            c['trip'] = trips[0]
        return render_to_response('profile.html', c)
    else:
        return redirect("/")

def logout(request):
    del request.session['facebook_id']
    if "access_token" in request.session:
        del request.session['access_token']
    del request.session['first_name']
    del request.session['last_name']
    return redirect("/")

def populate_database(request):
    types1 = ["amusement_park", "art_gallery", "library", "museum", "night_club", "park", "shopping_mall", "zoo", "stadium"]
    types2 = ["stadium", "movie_theater"]
    for t in types2:
        query_string = GOOGLE_PLACES_BASE_STRING + COLUMBIA_LAT + "," + COLUMBIA_LONG +"&radius=10000&types=" + t + "&sensor=false&key=" + GOOGLE_API_KEY
        data = requests.get(query_string).json()
        for location in data['results']:
            if (len(Location.objects.filter(name=location['name'])) == 0):
                if 'rating' in location:
                    rating = location['rating']
                else:
                    rating = "N/A"
                if 'photos' in location:
                    photo_ref = location['photos'][0]['photo_reference']
                else:
                    photo_ref = "N/A"
                reference= location['reference']
                details_string = GOOGLE_DETAILS_BASE_STRING + reference + "&sensor=false&key=" + GOOGLE_API_KEY
                details = requests.get(details_string).json()
                if 'website' in details['result']:
                    website = details['result']['website']
                else:
                    website = "N/A"
                new_location = Location.create(location['name'],location['geometry']['location']['lat'],location['geometry']['location']['lng'],location['vicinity'],rating,photo_ref,location['types'][0],reference,website)
                new_location.save()
    return HttpResponse("Success!")

def places(request):
    museums = get_museums()
    c={}
    c["museums"] = museums
    c["size"] = len(museums)
    return render_to_response('places.html', c)

def get_orbit_data():
    museum_search = Location.objects.filter(location_type="museum").exclude(photo_reference="N/A").exclude(website="N/A")
    park_search = Location.objects.filter(location_type="park").exclude(photo_reference="N/A").exclude(website="N/A")
    art_search = Location.objects.filter(location_type="art_gallery").exclude(photo_reference="N/A").exclude(website="N/A")
    night_club_search = Location.objects.filter(location_type="night_club").exclude(photo_reference="N/A").exclude(website="N/A")
    objects = []
    random_id = random.randint(0, len(museum_search) - 1)
    objects.append(museum_search[random_id])
    random_id = random.randint(0, len(park_search) - 1)
    objects.append(park_search[random_id])
    random_id = random.randint(0, len(art_search) - 1)
    objects.append(art_search[random_id])
    random_id = random.randint(0, len(night_club_search) - 1)
    objects.append(night_club_search[random_id])
    places = []
    for place in objects:
        name = place.name
        address = place.address
        photo = place.photo_reference
        my_place = {}
        my_place["name"] = name
        my_place["address"] = address
        photo_link = "https://maps.googleapis.com/maps/api/place/photo?photo_reference=" + photo + "&key=" + GOOGLE_API_KEY + "&sensor=false&maxheight=300"
        my_place["photo"] = photo_link
        my_place["website"] = place.website
        places.append(my_place)
    return places

def profile_upcoming_events():
    query_string = NEW_YORK_TIMES_BASE_STRING + "&ll=" + COLUMBIA_LAT + "," + COLUMBIA_LONG +"&radius=1000&limit=5"
    query_results = requests.get(query_string).json()
    events = process_nytimes_results(query_results)
    return events

def get_location():
    locations = Location.objects.all().exclude(photo_reference="N/A")
    rand_index = random.randint(0, len(locations) - 1)
    location = locations[rand_index]
    loc = {}
    loc['name'] = location.name
    loc['address'] = location.address
    photo = location.photo_reference
    photo_link = "https://maps.googleapis.com/maps/api/place/photo?photoreference=" + photo + "&key=" + GOOGLE_API_KEY + "&sensor=false&maxheight=200"
    loc['photo'] = photo_link
    loc['reference'] = location.reference
    loc['website'] = location.website
    return loc

def planner(request):
    if 'facebook_id' in request.session:
        c = {}
        c['facebook_id'] = request.session['facebook_id']
        c['first_name'] = request.session['first_name']
        c['last_name'] = request.session['last_name']
        data = request.GET.copy()
        if 'loc' in data:
            request.session['loc'] = data['loc']
            if 'event' in request.session:
                del request.session['event']
            if 'restaurant' in request.session:
                del request.session['restaurant']
            return redirect("/planner/")
        if 'event' in data:
            request.session['event'] = data['event']
            if 'restaurant' in request.session:
                del request.session['restaurant']
            return redirect("/planner/")
        if 'restaurant' in data:
            request.session['restaurant'] = data['restaurant']
            if 'loc' in request.session:
                if 'event' in request.session:
                    return redirect("/finalize/")
        c['facebook_id'] = request.session['facebook_id']
        c['first_name'] = request.session['first_name']
        c['last_name'] = request.session['last_name']
        if 'loc' in request.session:
            if 'event' in request.session:
                # Have location and event, need to get restaurant
                event = request.session['event']
                this_event = Event.objects.filter(event_id=event)
                if (len(this_event) != 1):
                    return HttpResponse("FUCK THIS")
                else:
                    my_event = this_event[0]
                    address = my_event.street_address + ", " + my_event.city + ", " + my_event.state
                    address = address.replace(" ", "+")
                    coord_query = GEOCODING_BASE_STRING + address +"&sensor=false"
                    coord_results = requests.get(coord_query).json()
                    if (len(coord_results) == 0):
                        return HttpResponse("FUCK THIS")
                    else:
                        loc = coord_results["results"][0]
                        lat = loc['geometry']['location']['lat']
                        lng = loc['geometry']['location']['lng']
                        restaurants = process_restaurant_results(lat,lng)
                        length = len(restaurants)
                        my_restaurants = []
                        count = 0
                        while count < 3:
                            rand_index = random.randint(0,length-1)
                            my_restaurants.append(restaurants[rand_index])
                            count = count + 1
                        c['restaurants'] = my_restaurants
                        return render_to_response("restaurant.html",c) 
                return render_to_response('restaurant.html', c)
            else:
                # Have location, need to get event
                location = Location.objects.filter(reference=request.session['loc'])
                if (len(location) == 1):
                    loc = location[0]
                    ny_times_query = NEW_YORK_TIMES_BASE_STRING + "&ll=" + loc.latitude + "," + loc.longitude +"&radius=1000&limit=10"
                    ny_times_results = requests.get(ny_times_query).json()
                    events = process_nytimes_results(ny_times_results)
                    c['events'] = events
                    return render_to_response('event.html',c)
                return HttpResponse("FUCK")
        locs = []
        count = 0
        while (count < 3):
            locs.append(get_location())
            count = count + 1
            c['locations'] = locs
        return render_to_response('location.html', c)
    else:
        return redirect("/")
    
def start_over(request):
    if 'loc' in request.session:
        del request.session['loc']
    if 'event' in request.session:
        del request.session['event']
    if 'restaurant' in request.session:
        del request.session['restaurant']
    return redirect("/planner/")

def process_nytimes_results(nytimes):
    events = []
    for result in nytimes["results"]:
        event = {}
        event['id'] = result['event_id']
        event['name'] = result['event_name']
        event['link'] = result['event_detail_url']
        if "venue_name" in result:
            event['location'] = result['venue_name']
        else:
            event['location'] = "N/A"
        description = result['web_description']
        event['description'] = description
        if 'telephone' in result:
            event['phone_number'] = result['telephone']
        else:
            event['phone_number'] = "N/A"
        event['street_address'] = result['street_address']
        event['city'] = result['city']
        event['state'] = result['state']
        if 'postal_code' in result:
            event['postal_code'] = result['postal_code']
        else:
            event['postal_code'] = "N/A"
        if (len(Event.objects.filter(event_id=event['id'])) == 0):
            my_event = Event.create(event['name'],event['id'],event['link'],event['location'],event['phone_number'],event['street_address'],event['city'],event['state'],event['postal_code'])
            my_event.save()
        events.append(event)
    return events

def process_restaurant_results(lat,lng):
    query_string = GOOGLE_PLACES_BASE_STRING + str(lat) + "," + str(lng) + "&types=restaurant&key=" + GOOGLE_API_KEY + "&radius=1000&sensor=false" 
    results = requests.get(query_string).json()
    restaurants = []
    for result in results['results']:
        my_reference = result['reference']
        if (len(Restaurant.objects.filter(reference=my_reference)) == 0):
            name = result['name']
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']
            address = result['vicinity']
            if 'ranking' in result:
                ranking = result['rating']
            else:
                ranking = "N/A"
            if 'photos' in result:
                photo_reference = result['photos'][0]['photo_reference']
            else:
                photo_reference = "N/A"
            reference = result['reference']
            details_string = GOOGLE_DETAILS_BASE_STRING + reference + "&key=" + GOOGLE_API_KEY + "&sensor=false"
            details = requests.get(details_string).json()
            if 'result' in details:
                detail = details['result']
                if 'website' in detail:
                    website = detail['website']
                else:
                    website = "N/A"
            else:
                website = "N/A"
            if 'price_level' in result:
                price = result['price_level']
            else:
                price = "N/A"
            restaurant = Restaurant.create(name,lat,lng,address,ranking,photo_reference,reference,website,price)
            restaurant.save()
            new_restaurant = {}
            new_restaurant['name'] = name
            new_restaurant['website'] = website
            new_restaurant['address'] = address
            new_restaurant['reference'] = reference
            if photo_reference != "N/A":
                photo_link = "https://maps.googleapis.com/maps/api/place/photo?photoreference=" + photo_reference+ "&key=" + GOOGLE_API_KEY + "&sensor=false&maxheight=200"
                new_restaurant['photo'] = photo_link
                restaurants.append(new_restaurant)
    return restaurants

def finalize(request):
    if 'facebook_id' in request.session:
        c={}
        c['facebook_id'] = request.session['facebook_id']
        c['first_name'] = request.session['first_name']
        c['last_name'] = request.session['last_name']
        if 'loc' in request.session and 'event' in request.session and 'restaurant' in request.session:
            location = Location.objects.filter(reference=request.session['loc'])
            if (len(location) >= 0):
                c['location'] = location[0]
            event = Event.objects.filter(event_id=request.session['event'])
            if (len(event) >= 0):
                c['event'] = event[0]
            restaurant = Restaurant.objects.filter(reference=request.session['restaurant'])
            if (len(restaurant) >= 0):
                c['restaurant'] = restaurant[0]
            map_link = GOOGLE_MAPS_BASE_STRING + "&size=400x400&maptype=roadmap&"
            map_link = map_link + "markers=color:blue%7Clabel:L%7C" + c['location'].latitude + "," + c['location'].longitude
            event_coordinates = get_coordinates(c['event'])
            map_link = map_link + "&markers=color:green%7Clabel:E%7C" + str(event_coordinates['lat']) + "," + str(event_coordinates['long'])
            map_link = map_link + "&markers=color:red%7Clabel:R%7C" + c['restaurant'].latitude + "," + c['restaurant'].longitude
            map_link = map_link + "&sensor=false"
            c['map'] = map_link
            return render_to_response("finalize.html",c)
        else:
            return HttpResponse("FUCK THIS")
    else:
        return redirect("/")

def create_event(request):
    if 'facebook_id' in request.session:
        c = {}
        c['facebook_id'] = request.session['facebook_id']
        c['first_name'] = request.session['first_name']
        c['last_name'] = request.session['last_name']
        facebook_id = request.session['facebook_id']
        facebook_user = FacebookUser.objects.filter(facebook_id=facebook_id)[0]
        if 'loc' in request.session and 'event' in request.session and 'restaurant' in request.session:
            location = Location.objects.filter(reference=request.session['loc'])[0]
            event = Event.objects.filter(event_id=request.session['event'])[0]
            restaurant = Restaurant.objects.filter(reference=request.session['restaurant'])[0]
            del request.session['loc']
            del request.session['event']
            del request.session['restaurant']
            graph = GraphAPI(request.session['access_token'])
            event_name = "Trip to " + location.name
            description = "We will be going to " + location.name + ". " + "We will then be going to " + event.name + ". Then we will eat at " + restaurant.name +". This event has been created with PlanMyNY."
            sample_event = graph.post('me/events', params={"name":event_name, "description":description, "location":"New York City","start_time":"2014-02-09T16:00-5:00", "end_time":"2014-02-09T23:00-5:00", "privacy_type":"FRIENDS"})
            event_id = sample_event['id']
            c['event_link'] = "http://www.facebook.com/events/" + event_id
            trip = Trip.create(facebook_user,location,event,restaurant,c['event_link'])
            trip.save()
            return render_to_response("success.html", c)
        else:
            return redirect("profile/")
    else:
        return redirect("/")
            

def get_coordinates(my_event):
    c={}
    address = my_event.street_address + ", " + my_event.city + ", " + my_event.state
    address = address.replace(" ", "+")
    coord_query = GEOCODING_BASE_STRING + address +"&sensor=false"
    coord_results = requests.get(coord_query).json()
    if (len(coord_results) == 0):
        return c
    else:
        loc = coord_results["results"][0]
        lat = loc['geometry']['location']['lat']
        lng = loc['geometry']['location']['lng']
        c['lat'] = lat
        c['long'] = lng
        return c


    
    
