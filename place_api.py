import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_PLACE_API_KEY')


def find_place(inputText, lat, lng):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    inputType = 'textquery'
    language = 'zh-TW'
    fields = [
        'place_id',
        'formatted_address',
        'geometry',
        'name',
        'photo'
    ]
    params = {
        'input': inputText,
        'inputtype': inputType,
        'fields': ','.join(fields),
        'language': language,
        'locationbias': f'point:{lat},{lng}',
        'key': api_key
    }
    response = requests.get(url, params=params)
    return response.json()


if __name__ == '__main__':
    from pprint import pprint
    query = '7-11'
    pprint(find_place(query))
