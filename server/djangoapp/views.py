from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, reverse
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_dealer_review
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
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
        return render(request, "djangoapp/about.html", context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/contact_us.html", context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return HttpResponseRedirect(reverse(viewname="djangoapp:index"))
    else:
        return redirect("djangoapp:index")

# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to homepage
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)

    elif request.method == "POST":
        username = request.POST["username"]
        password = make_password(request.POST["psw"])
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse(viewname="djangoapp:index"))
        else:
            return render(request, "djangoapp/registration.html")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/Bhumbla_Coursera/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # Get dealership details
        dealership_url = "https://us-south.functions.appdomain.cloud/api/v1/web/Bhumbla_Coursera/dealership-package/get-dealership"
        dealership = get_dealer_by_id_from_cf(dealership_url, dealer_id)[0]
        context["dealership_details"] = dealership
        
        # Get all reviews of dealership
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/Bhumbla_Coursera/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["review_list"] = reviews
        
        return render(request, "djangoapp/dealer_details.html", context)
# ...

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.user.is_authenticated is not True:
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    
    dealership_url = "https://us-south.functions.appdomain.cloud/api/v1/web/Bhumbla_Coursera/dealership-package/get-dealership"
    dealership = get_dealer_by_id_from_cf(dealership_url, dealer_id)[0]
    context["dealership_details"] = dealership
    if request.method == "POST":
        #dealer_id = request.POST["dealership"]
        # Add new Review
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/Bhumbla_Coursera/dealership-package/post-review"
        new_review= dict()
        new_review["name"] = request.user.first_name + " " + request.user.last_name
        new_review["review"] = request.POST["content"]
        new_review["purchase"] = True if request.POST["purchasecheck"] == "on" else False
        new_review["purchase_date"] = request.POST["purchasedate"]
        car_details = CarModel.objects.get(id=request.POST["car"])
        new_review["car_make"]= car_details.make.name
        new_review["car_model"]= car_details.name
        new_review["car_year"]= car_details.year.strftime("%Y")
        new_review["dealership"] = dealer_id
        new_review["time"] = datetime.utcnow().isoformat()
        #print(new_review.values())
        json_payload = dict()
        json_payload["review"] = new_review
        post_dealer_review(review_url, json_payload, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        # Get cars for the dealer
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"] = cars
        return render(request, "djangoapp/add_review.html", context)
# ...

