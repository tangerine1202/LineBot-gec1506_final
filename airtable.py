import os
from dotenv import load_dotenv
from pyairtable import Table

load_dotenv()

def create(place):
	
	return table.create(place)

def getAll():
	api_key = os.environ['AIRTABLE_API_KEY']
	base_id = os.environ['AIRTABLE_BASE_ID']
	table_name = 'Places'
	table = Table(api_key, base_id, table_name)
	table.all()
	records = table.all()
	return {'total':len(records),'data':records}

if __name__ == '__main__':
    from pprint import pprint
	place = {
        'address': 'sample_address', 
        'name': 'sample_name',
        'place_id': 'sample_place_id'
    }
    res = table.create(place)
    pprint(res)
