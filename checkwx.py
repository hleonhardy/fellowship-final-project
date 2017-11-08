import os
import requests


API_KEY = os.environ['CHECKWXAPIKEY']

#Zulu time is 24hr UTC

def return_forecast_dict(icao):
    """prints forecast times and clouds"""

    url = 'https://api.checkwx.com/taf/{}/decoded'.format(icao)
    headers = { 'X-API-Key': API_KEY }

    response = requests.get(url, headers=headers)
    json_response = response.json()

    data = json_response['data']

    #I guess data was a list with only one item (dictionary)
    #So now it is a dictionary:
    data = data[0]

    #Getting a list of all forecasts
    #Each index in the list is the forecast(dictionary)
    forecasts = data['forecast']

    # for forecast_dict in forecasts:

    #     timestamp = forecast_dict['timestamp']
    #     forecast_to = timestamp['forecast_to']
    #     forecast_from = timestamp['forecast_from']

    #     clouds_list = forecast_dict['clouds']

    #     print "Forecast FROM: {}\nForecast TO: {}".format(forecast_from, forecast_to)

    #     for item in clouds_list:
    #         cloud_type = item['code']
    #         cloud_height = item['base_feet_agl']

    #         print "{} @ {} ft.".format(cloud_type, cloud_height)
    #     print

    return forecasts



# print_response('cyvr')
