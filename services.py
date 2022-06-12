import os
from pprint import pprint

from dotenv import load_dotenv
from pyairtable import Table

from placeApi import find_place


load_dotenv()

api_key = os.getenv('AIRTABLE_API_KEY')
base_id = os.getenv('AIRTABLE_BASE_ID')

user_table = Table(api_key, base_id, 'Users')
place_table = Table(api_key, base_id, 'Places')
join_table = Table(api_key, base_id, 'UserPlaceJoin')


def greeting(line_id):
    result = {'name': line_id}
    return result


def google(text, lat, lng):
    res = find_place(text, lat, lng)
    res = res['candidates'][0]

    place_id = res['place_id']
    name = res['name']
    address = res['formatted_address']
    result = {
        'place_id': place_id,
        'name': name,
        'address': address
    }
    return result


def get_user_from_line_id(line_id):
    formula = f'FIND("{line_id}", line_id)'
    res = user_table.first(formula=formula)
    if not res:
        print('[error]: User not found')
        res = None
    result = {'id': res['id'], }
    for key, value in res['fields'].items():
        result[key] = value
    return result


def add_user(line_id):
    default = {
        'lat': 24.796121,
        'lng': 120.996669,
    }
    fields = {
        'line_id': line_id,
        'lat': str(default['lat']),
        'lng': str(default['lng']),
    }
    res = user_table.create(fields)
    lat, lng = default['lat'], default['lng']
    result = {
        'lat': lat,
        'lng': lng,
    }
    return result


def set_location(user_id, lat, lng):
    fields = {
        'lat': str(lat),
        'lng': str(lng)
    }
    res = user_table.update(user_id, fields)
    result = {
        'lat': lat,
        'lng': lng,
    }
    return result

def add_place(line_id, lat, lng, name):
    a = google(name, lat, lng)
    i = place_table.all()
    x = 1
    for item in i:
        if a['place_id'] == item['fields']['place_id']:
            x = 0

    if x == 1:
        place_table.create(a)

    j = join_table.all(fields = ['line_id', 'place_id'])

    x = 0
    for item in j:
        if a['place_id'] == item['fields']['place_id'] and line_id == item['fields']['line_id']:
            x = 1
    
    if x == 0:
        join_table.create({'line_id': line_id, 'place_id': a['place_id'], 'nickname': name})

    result = {
        'name': a['name'],
        'address': a['address']
    }
    return result