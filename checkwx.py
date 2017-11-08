import os
import requests


API_KEY = os.environ['CHECKWXAPIKEY']

url = 'https://api.checkwx.com/metar/lat/51.4706/lon/-1.461941/decoded'
headers = {API_KEY: '{key}'}

response = requests.get(url, headers=headers)

print response
