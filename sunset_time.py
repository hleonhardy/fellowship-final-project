from urllib2 import urlopen
from json import load
import datetime

#SOURCE: https://sunrise-sunset.org/api

def return_sunset_time(lat, lon, date="today"):
    """Returns time of sunset given coordinates and date"""

    url = "https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}".format(
            lat, lon, date)

    response = urlopen(url)
    json_obj = load(response)

    sunset_utc = json_obj['results']['sunset']

    return sunset_utc


sfo_lat = 37.6189994812012
sfo_lon = -122.375

print return_sunset_time(sfo_lat, sfo_lon)
