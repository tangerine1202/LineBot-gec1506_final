import os
import requests
from dotenv import load_dotenv

# load your .env file
load_dotenv()

# call Google findPlace API
# inputText: query string
def findPlace(inputText):
    # url of the api
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    inputType = 'textquery'
    language = 'zh-TW'
    # the fields we wanted
    fields = [
        'place_id',
        'formatted_address',
        'geometry',
        'name',
        'photo'
    ]

# format parameters
    params = {
        'input': inputText,
        'inputtype': inputType,
        'fields': ','.join(fields),
        'language': language,
        'key': os.getenv('GOOGLE_PLACE_API_KEY')
    }
	
    # send request and get the response
    response = requests.get(url, params=params)
	
    # parse response from json format into python dictionary
    return response.json()

if __name__ == '__main__':
    from pprint import pprint
    query = '7-11'
    pprint(findPlace(query))