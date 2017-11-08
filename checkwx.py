import os
import requests


API_KEY = os.environ['CHECKWXAPIKEY']

def print_response(icao):

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

    for forecast_dict in forecasts:

        timestamp = forecast_dict['timestamp']
        forecast_to = timestamp['forecast_to']
        forecast_from = timestamp['forecast_from']

        clouds_list = forecast_dict['clouds']

        print "Forecast TO: {} \n Forecast FROM: {}".format(forecast_to, forecast_from)
        
        for item in clouds_list:
            cloud_type = item['code']
            cloud_height = item['base_feet_agl']

            print "{} @ {} ft.".format(cloud_type, cloud_height)
        print


print_response('ksea')
