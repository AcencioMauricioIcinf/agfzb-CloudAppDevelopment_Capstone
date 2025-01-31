from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, analyze_review_sentiments, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            user_exist = False
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fcc6f7b6-c4ad-4067-a0a1-0287f313fa64/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        
        context['dealerships'] = dealerships
        
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fcc6f7b6-c4ad-4067-a0a1-0287f313fa64/dealership-package/get-review"
        # Get dealers from the URL
        reviews = get_dealer_by_id_from_cf(url, dealer_id)
        context = { 'dealer_id': dealer_id }
        for i in range(len(reviews)):
            sentiment = analyze_review_sentiments(reviews[i].review)
            reviews[i].sentiment = sentiment
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = { 'dealer_id': dealer_id }
    if request.method == 'GET':
        context['cars'] = CarModel.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST' and request.user.is_authenticated:
        payload = {}
        payload['review'] = {}
        payload['review']["review"] = request.POST["review"]
        payload['review']["dealership"] = dealer_id
        payload['review']["time"] = datetime.utcnow().isoformat()
        name = request.user.first_name + ' ' + request.user.last_name
        payload['review']["name"] = name if name.strip() else request.user.username
        payload['review']["purchase"] = bool(request.POST.get("purchasecheck"))
        if request.POST.get("purchasecheck"):
            payload['review']["purchase_date"] = request.POST["purchasedate"]
            car_id = request.POST["car"]
            car_obj = CarModel.objects.get(pk=car_id)
            payload['review']["car_make"] = car_obj.car_make.name
            payload['review']["car_model"] = car_obj.name
            payload['review']["year"] = car_obj.year.isoformat()
        
        print(json.dumps(payload['review'], indent=2))
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/fcc6f7b6-c4ad-4067-a0a1-0287f313fa64/dealership-package/post-review'
        post_request(url=url, json_payload=payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)        
