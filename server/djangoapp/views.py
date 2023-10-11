from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

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
        else:
            context['message'] = "Invalid Username or Password"
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/710ea3b4-6b8b-4d48-bc2f-76a574cc475d/dealership-package/get-dealerships"
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        return render(request, "djangoapp/index.html", context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {"dealer_id":dealer_id}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/710ea3b4-6b8b-4d48-bc2f-76a574cc475d/dealership-package/get_reviews"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews

        url2 = "https://us-south.functions.appdomain.cloud/api/v1/web/710ea3b4-6b8b-4d48-bc2f-76a574cc475d/dealership-package/get-dealerships"
        dealer = get_dealer_by_id_from_cf(url2, dealer_id)
        context['dealer'] = dealer
        
        return render(request, 'djangoapp/dealer_details.html', context)

# View to submit a review
def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        print("User is not authenticated")
        return request.redirect("djangoapp:index")

    if request.method == "GET":
        context = {"dealer_id": dealer_id}
        cars = list(CarModel.objects.filter(dealerID=dealer_id))
        for car in cars:
            car.year = str(str(car.year).split('-')[0])
        context["cars"] = cars
        url1 = "https://us-south.functions.appdomain.cloud/api/v1/web/710ea3b4-6b8b-4d48-bc2f-76a574cc475d/dealership-package/get-dealerships"
        dealer = get_dealer_by_id_from_cf(url1, dealer_id)
        context["dealer"] = dealer
        return render(request, "djangoapp/add_review.html", context)
        
    if request.method == "POST":
        url2 = "https://us-south.functions.appdomain.cloud/api/v1/web/710ea3b4-6b8b-4d48-bc2f-76a574cc475d/dealership-package/post-review"
        review = {}
        car_id = request.POST["car"]
        car = CarModel.objects.get(pk=car_id)
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["name"] = request.user.username
        review["review"] = request.POST["content"]
        review["id"] = dealer_id

        if "purchasecheck" in request.POST and request.POST["purchasecheck"] == "on":
            review["purchase"] = True
        else:
            review["purchase"] = False
        review["purchase_date"] = request.POST["purchasedate"]
        review["car_make"] = car.modelId.name
        review["car_model"] = car.name
        review["car_year"] = int(car.year.strftime("%Y"))

        json_payload ={"review" : review}
        post_request(url2, json_payload, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)