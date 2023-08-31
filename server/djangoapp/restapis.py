import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from .nlu import analyze_text


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    json_data = []
    try:
        # Call get method of requests library with URL and parameters
        if api_key is None:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        else:
            print(api_key)
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, api_key=None, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    json_data = []
    try:
        # Call get method of requests library with URL and parameters
        if api_key is None:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    json=json_payload, params=kwargs)
        else:
            print(api_key)
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    json=json_payload, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_state(url, state):
    return get_dealers_from_cf(url, state=state)

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealer_id):
    results = []
    response = get_request(url, dealerId=dealer_id)
    if response:
        for review in response:
            
            review_obj = DealerReview(
                review['dealership'],
                review['name'],
                review['purchase'],
                review['review'],
                review.get('purchase_date'),
                review.get('car_make'),
                review.get('car_model'),
                review.get('car_year'),
                '',
                review.get('id'),
            )
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review):
    result = analyze_text(review)
    print(result)
    if len(result['entities']) == 0:
        return 'neutral'
    else:
        return result['entities'][0]['sentiment']['label']
    


