import datetime
from checkwx import return_forecast_dict
from sunset_time import return_sunset_time
from errors import NoForecastDataError


def today_or_tomorrow_sunset(lat, lon):
    """determines if you should use todays or tomorrows sunset and gives the coordinates"""

    current_date = datetime.date.today()

    #Find sunset time local to given airport
    # import pdb; pdb.set_trace()
    sunset_time_today = return_sunset_time(lat, lon, current_date)


    #getting current UTC time datetime object to compare to sunset datetime
    current_utc = datetime.datetime.utcnow()
    # print current_utc

    #Creating datetime objects with strptime:
    #'2017-11-09T01:03:37+00:00' is the format for the sunet time.
    sunset_time_today_obj = datetime.datetime.strptime(sunset_time_today,
                                                       '%Y-%m-%dT%H:%M:%S+00:00')

    #If Sunset has already passed, we want to give you tomorrow's time.
    if sunset_time_today_obj > current_utc:
        sunset_time_obj = sunset_time_today_obj

    else:
        #Getting tomorrow's date:
        tomorrow = current_utc + datetime.timedelta(days=1)
        #Getting sunset time using tomorrow's date
        sunset_time_tomorrow = return_sunset_time(lat, lon, tomorrow)
        #Setting the sunset time = tomorrow's sunset time
        sunset_time_obj = datetime.datetime.strptime(sunset_time_tomorrow,
                                                     '%Y-%m-%dT%H:%M:%S+00:00')

    return sunset_time_obj



def find_forecast(code, sunset_time_obj):
    """Given icao code and sunset_time_obj: returns correct forecast in JSON"""


    try:
        #Airport class requires upper case icao,
        #CheckWX API requires lowercase
        #Getting the dictionary which contains multiple forecasts:
        forecast_dict = return_forecast_dict(code.lower())
    except:
        raise NoForecastDataError("No forecast available")

    #Going through the dictionary and picking the forecast that matches
    #The sunset time
    for forecast in forecast_dict:
        #Starting Time:
        forecast_from = forecast['timestamp']['forecast_from']
        #Ending Time:
        forecast_to = forecast['timestamp']['forecast_to']
        #Making forecasts into datetime objects
        #In order to compare to the sunset time:
        forecast_from_obj = datetime.datetime.strptime(forecast_from,
                                                       '%d-%m-%Y @ %H:%MZ')
        forecast_to_obj = datetime.datetime.strptime(forecast_to,
                                                       '%d-%m-%Y @ %H:%MZ')
        #We want the sunset time that is within the forecast range:
        if sunset_time_obj >= forecast_from_obj and sunset_time_obj < forecast_to_obj:
            #The correct forecast
            sunset_forecast_json = forecast
            break


    return sunset_forecast_json



# sfo_lat = 37.6189994812012
# sfo_lon = -122.375
# sfo_code = 'KSFO'

# sunset_date_obj = today_or_tomorrow_sunset(sfo_lat, sfo_lon)
# forecast_json = find_forecast(sfo_code, sunset_date_obj)

# print forecast_json

