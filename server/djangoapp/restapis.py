import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url)
    # - Parse JSON results into a CarDealer object list
    if json_result:
        dealerships = json_result
        for dealer in dealerships:
            dealer_details = dealer['doc']
            dealer_obj = CarDealer(
                address=dealer_details['address'],
                city=dealer_details['city'],
                full_name=dealer_details['full_name'],
                id=dealer_details['id'],
                lat=dealer_details['lat'],
                long=dealer_details['long'],
                short_name=dealer_details['short_name'],
                st=dealer_details['st'],
                zip=dealer_details['zip'],
            )
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function

def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url, dealerId=dealerId)
    # - Parse JSON results into a CarDealer object list
    if json_result:
        dealerships = json_result
        for dealer_details in dealerships:
            dealer_obj = CarDealer(
                address=dealer_details['address'],
                city=dealer_details['city'],
                full_name=dealer_details['full_name'],
                id=dealer_details['id'],
                lat=dealer_details['lat'],
                long=dealer_details['long'],
                short_name=dealer_details['short_name'],
                st=dealer_details['st'],
                zip=dealer_details['zip'],
            )
            results.append(dealer_obj)
    return results

def get_dealer_by_state_from_cf(url, state):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url, state=state)
    # - Parse JSON results into a CarDealer object list
    if json_result:
        dealerships = json_result
        for dealer_details in dealerships:
            dealer_obj = CarDealer(
                address=dealer_details['address'],
                city=dealer_details['city'],
                full_name=dealer_details['full_name'],
                id=dealer_details['id'],
                lat=dealer_details['lat'],
                long=dealer_details['long'],
                short_name=dealer_details['short_name'],
                st=dealer_details['st'],
                zip=dealer_details['zip'],
            )
            results.append(dealer_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



