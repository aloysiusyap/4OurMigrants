import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class SearchEvents:
    def __init__(self):
        # API_KEY = os.getenv("_API_KEY")
        self.ENDPOINT = "https://api.stb.gov.sg/content/events/v2/search"
        self.HEADERS = {'x-api-key': '<api_key_goes_here>'}

    def search_events(self, searchType, searchValues):
        PARAMETERS = {'searchType': searchType,
                    'searchValues': searchValues
                    }

        response = requests.get(url = self.ENDPOINT,
                                params = PARAMETERS,
                                headers = self.HEADERS).json()['data']
        
        recommended_events = {}
        for event in response:
            recommended_events[event['name']] = {'description' : event['description'],
                                           'officialWebsite' : event['officialWebsite']}

        json_output = "*** List of recommended events based on " + searchValues + " ***\n\n"
        for k,v in recommended_events.items():
            json_output += f"Name: \t{k}\ndescription: \t{v['description']}\nofficialWebsite: \t{v['officialWebsite']}\n\n"

        return json_output
        # business_data = response.json()
        # return json.dumps(business_data, indent=4)
    

if __name__ == '__main__':
    results = SearchEvents().search_event(searchType='Keyword', searchValues='arts')
    print(results)
