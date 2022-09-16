import requests
import json
import os
from dotenv import load_dotenv
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

load_dotenv()

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
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
def post_request(url, payload, **kwargs):
    print("POST from {} ".format(url))
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, json=payload, params=kwargs )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

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
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url, dealerId=dealerId)

    if json_result:
        dealer_reviews = json_result['data']['docs']
        for review in dealer_reviews:
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                id=review["_id"],
                purchase=review["purchase"],
                purchase_date=review["purchase_date"],
                review=review["review"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=''
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results


def post_dealer_review(url, payload, **params):
    # - Call get_request() with specified arguments
    json_result = post_request(url, payload, **params)
    
    return json_result


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
def analyze_review_sentiments(text):
    url = os.getenv('IBM_WATSON_NLU_API_URL')

    api_key = os.getenv('IBM_WATSON_NLU_API_KEY')

    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 
    try:
        response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()

    except:
        return ('could not evaluate')

    label=json.dumps(response, indent=2) 

    # - Get the returned sentiment label such as Positive or Negative
    label = response['sentiment']['document']['label'] 

    return (label) 




