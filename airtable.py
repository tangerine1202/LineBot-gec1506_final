import os
from dotenv import load_dotenv
from pyairtable import Table
from pyairtable.formulas import match

load_dotenv()

def create(place):
	api_key = os.environ['AIRTABLE_API_KEY']
	base_id = os.environ['AIRTABLE_BASE_ID']
	table_name = 'Places'
	table = Table(api_key, base_id, table_name)
	place = table.get(base_id,table_name,)
	return table.create(place)

def getAll():
	api_key = os.environ['AIRTABLE_API_KEY']
	base_id = os.environ['AIRTABLE_BASE_ID']
	table_name = 'Places'
	table = Table(api_key, base_id, table_name)
	table.all()
	records = table.all()
	return {'total':len(records),'data':records}

#def getrec():
	#api_key = os.environ['AIRTABLE_API_KEY']
	#base_id = os.environ['AIRTABLE_BASE_ID']
	#table_name = 'UserPlaceJoin'
	#table = Table(api_key, base_id, table_name)
	#formula = match({"user_id":"u2"})
	#records = table.all(formula=formula)
	#return {'total':len(records),'data':records}

if __name__ == '__main__':
    from pprint import pprint
	#place = { 
        #'place_id': 'sample_place_id',
		#'name': 'sample_name',
		#'address': 'sample_address'
    #}
    res = getrec()
    pprint(res)
	
	
