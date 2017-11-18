import os
import requests
from errors import NoForecastDataError


API_KEY = os.environ['CHECKWXAPIKEY']

#Zulu time is 24hr UTC

def return_forecast_dict(icao_list):
    """prints forecast times and clouds"""

    #format string of icao_codes
    icao_string = ','.join(icao_list)
    print icao_string

    url = 'https://api.checkwx.com/taf/{}/decoded'.format(icao_string)
    headers = { 'X-API-Key': API_KEY }

    response = requests.get(url, headers=headers)
    json_response = response.json()

    #List of separate icao forecasts:
    #Each item in the data list corresponds to different icao code.
    #This comes in order of icao_string
    data = json_response['data']

    working_icao_forecasts = []

    for icao_data in data:
        print "THE DATA"
        print icao_data
        print "END OF DATA"

        #An airport with no forecast data will not have a forecast key.
        try:
            #Getting a list of all forecasts
            #Each index in the list is the forecast:
            #(list of individual forecast dictionaries)
            forecasts = icao_data['forecast']
            print "FORECAST EXISTS!"

        except:
            # raise NoForecastDataError('No forecast available')
            continue


        #Adding the icao to each forecast because it makes it easier
        #in the future to find the code if we do this now.
        #note: it seems unnecesary to be adding this to every forecast even
        #though we're going to throw out all but one of the forecasts
        #but we won't be able to add it to an individual one later on.
        for individual_forecast_dict in forecasts:
            individual_forecast_dict['icao'] = icao_data['icao']

        #If there is forecast data, we want to append it to our list to return
        working_icao_forecasts.append(forecasts)


    return working_icao_forecasts
















