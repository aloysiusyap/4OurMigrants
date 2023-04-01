import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class SearchResults:
    def __init__(self):
        API_KEY = os.getenv("YELP_API_KEY")
        self.ENDPOINT = "https://api.yelp.com/v3/businesses/search"
        self.HEADERS = {'Authorization': 'bearer %s' % API_KEY}

    def search_yelp(self, term, location, category):
        PARAMETERS = {'term': term,
                    'limit': 3,
                    'radius': 1000,
                    'location': "Singapore " + location,
                    'price': 1,
                    'categories': category}

        response = requests.get(url = self.ENDPOINT,
                                params = PARAMETERS,
                                headers = self.HEADERS).json()['businesses']

        recommended_restaurants = {}
        for restaurant in response:
            recommended_restaurants[restaurant['name']] = {'rating' : restaurant['rating'],
                                           'price' : restaurant['price'],
                                           'address' : restaurant['location']['display_address'][0],
                                           'zipcode' : restaurant['location']['display_address'][1],
                                           'is_closed' : restaurant['is_closed']}

        json_output = "*** List of recommended " + term + " @ " + location + " ***\n\n"
        for k,v in recommended_restaurants.items():
            json_output += f"Name: \t{k}\nRating: \t{v['rating']}\nPrice: \t{v['price']}\nAddress: \t{v['address']}, {v['zipcode']}\nOpen: \t{not v['is_closed']}\n\n"

        return json_output
        # business_data = response.json()
        # return json.dumps(business_data, indent=4)
    

if __name__ == '__main__':
    results = SearchResults().search_yelp(term='food', location='bukit timah', category='')
    print(results)