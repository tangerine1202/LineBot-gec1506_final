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

    place_id = res['place_id']
    nickname = res['name']
    
    add = {
        'place_id': place_id,
        'nickname': name,
        # 'user_id': user_id
    }
    join_table.create(add)
    return result


def get_user_from_line_id(line_id):
    formula = f'FIND("{line_id}", line_id)'
    res = user_table.first(formula=formula)
    if not res:
        print('[error]: User not found')
        result = None
    else:
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

def remove_place(name, line_id, lat, lng):
    place = find_place(name, lat, lng)
    place_id = place['candidates'][0]['place_id']
    for record in join_table.all():
        print(record)
        print(line_id)
        print(name)
        if record['fields']['nickname'] == name and record['fields']['user_id'] == line_id:
            join_table.delete(record['id'])
            return True
        elif record['fields']['user_id'] == line_id and record['fields']['place_id'] == place_id:
            join_table.delete(record['id'])
            return True
    return False