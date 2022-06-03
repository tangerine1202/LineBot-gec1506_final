import os
from dotenv import load_dotenv

# load env variables from .env file
load_dotenv()

keys = ['LINE_SECRET', 'LINE_ACCESS_TOKEN']
for key in keys:
    # get the env variables
    val = os.getenv(key)
    print(f'{key}: {val}')