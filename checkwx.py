import os
import requests
from errors import NoForecastDataError


API_KEY = os.environ['CHECKWXAPIKEY']

#Zulu time is 24hr UTC

def return_forecast_dict(icao):
    """prints forecast times and clouds"""

    url = 'https://api.checkwx.com/taf/{}/decoded'.format(icao)
    headers = { 'X-API-Key': API_KEY }

    response = requests.get(url, headers=headers)
    json_response = response.json()

    print json_response

    data = json_response['data']

    #I guess data was a list with only one item (dictionary)
    #So now it is a dictionary:
    data = data[0]

    #An airport with no forecast data will not have a forecast key.
    try:
        #Getting a list of all forecasts
        #Each index in the list is the forecast(dictionary)
        forecasts = data['forecast']
    except:
        raise NoForecastDataError('No forecast available')

    #adding the icao code to this dictionary so that we can reference it later
    forecasts['icao_code'] = icao


    return forecasts


