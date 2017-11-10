#https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
import os
from urllib2 import urlopen
from json import load


GOOGLE_MAPS_API_KEY = os.environ['GOOGLEMAPSAPIKEY']


def get_coordinates_from_address(address):
    """Takes in an address string and returns coordinates using google maps api"""

    #giving the address the correct format for api
    #words/numbers separated by +s
    address = address.split()
    address = '+'.join(address)

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, GOOGLE_MAPS_API_KEY)
    response = urlopen(url)
    json_obj = load(response)

    #{u'status': u'OK', u'results': [{u'geometry': {u'location': {u'lat': 37.7886679, u'lng': -122.4114987},

    result = json_obj['results'][0]
    location = result['geometry']['location']

    lat = location['lat']
    lng = location['lng']

    return [lat, lng]



# address = '683 Sutter St, San Francisco, CA'
# print get_coordinates_from_address(address)