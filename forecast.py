import datetime
from checkwx import return_forecast_dict
from sunset_time import return_sunset_time
from errors import NoForecastDataError
import pprint

from model import connect_to_db, db, Airport

from flask import (Flask,
                   session,
                   jsonify)


def today_or_tomorrow_sunset(lat, lon):
    """determines if you should use todays or tomorrows sunset and gives the coordinates"""


    current_date = datetime.date.today()

    #Find sunset time local to given airport
    # import pdb; pdb.set_trace()
    sunset_time_today = return_sunset_time(lat, lon, current_date)

    # import pdb; pdb.set_trace()

    #getting current UTC time datetime object to compare to sunset datetime
    current_utc = datetime.datetime.utcnow()
    # print current_utc

    #Creating datetime objects with strptime:
    #'2017-11-09T01:03:37+00:00' is the format for the sunet time.
    sunset_time_today_obj = datetime.datetime.strptime(sunset_time_today,
                                                       '%Y-%m-%dT%H:%M:%S+00:00')

    #If Sunset has already passed, we want to give you tomorrow's time.
    #sunset_time greater means the sunset has NOT happened already, so use today.
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




def find_forecast(lst_of_forecast_dicts, sunset_time_obj):
    """Given icao code and sunset_time_obj: returns correct forecast in JSON"""


    # try:
    #     #Airport class requires upper case icao,
    #     #CheckWX API requires lowercase
    #     #Getting the dictionary which contains multiple forecasts:
    #     forecast_dict = return_forecast_dict(code.lower())
    #     print "FORECAST DICTIONARY:"
    #     print forecast_dict
    # except:
    #     raise NoForecastDataError("No forecast available")

    #Going through the dictionary and picking the forecast that matches
    #The sunset time

    print "sunset time: {}".format(sunset_time_obj)

    sunset_forecast_json = None

    for forecast in lst_of_forecast_dicts:
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

        print "forecast from: {} \n forecast to: {}".format(forecast_from_obj, forecast_to_obj)


        #We want the sunset time that is within the forecast range:
        if sunset_time_obj >= forecast_from_obj and sunset_time_obj < forecast_to_obj:
            #The correct forecast
            sunset_forecast_json = forecast
            break
        else:
            print "no forecasts in the available range?"

    if sunset_forecast_json is None:
        #using the last forecast available (latest)
        print "using latest possible forecast, although not in range."
        sunset_forecast_json = forecast

    #adding icao code to the dictionary so that we can reference it later on
    #commented out becuase of change in return_forecast_dict
    # sunset_forecast_json['icao'] = code


    return sunset_forecast_json



# sfo_lat = 37.721298
# sfo_lon = -122.221001
# sfo_code = 'KOAK'

# sunset_date_obj = today_or_tomorrow_sunset(sfo_lat, sfo_lon)
# print sunset_date_obj
# forecast_json = find_forecast(sfo_code, sunset_date_obj)

# print forecast_json




def find_nearest_airport_forecast(user_point):
    """Finds closest airport where the weather forecast is available and returns json response"""

#   #distance in meters
    distance = 1000000
    #limit on number of rows we get back from the query
    lim = 10

    sql_args = {'user_point': user_point, 'dist': distance, 'lim':lim}

    sql = """SELECT icao_code FROM airports
            WHERE ST_DWithin(location, :user_point, :dist)
            ORDER BY ST_Distance(location, :user_point)
            LIMIT :lim"""

    cursor = db.session.execute(sql, sql_args)

    #Getting all of the icao_codes from our database query:
    all_codes = cursor.fetchall()

    icao_code_lst = []

    #Putting all the codes in a list to send off to get forecasts for
    for icao_code in all_codes:
        #icao_code is (u'XXXX', )
        #so we need to get the 0th item out of there to get the code
        icao_code = icao_code[0]
        print icao_code
        icao_code_lst.append(icao_code.lower())

    #one giant list containing lists of all forecasts for one airport
    #make this into try and except to account for the no airports in range error

    try:
        all_icao_forecasts = return_forecast_dict(icao_code_lst)

    except:
        raise NoForecastDataError('No Forecasts Available')


    sunset_forecasts = []

    #for list of all forecasts for one airport in giant list:
    for lst_of_forecast_dicts in all_icao_forecasts:

        icao_code = lst_of_forecast_dicts[0]['icao']
        airport_obj = Airport.query.filter(Airport.icao_code == icao_code).one()

        #getting coordinates in order to find sunset time:
        lat = airport_obj.lattitude
        lng = airport_obj.longitude

        #Finding time of sunset
        sunset_datetime_obj = today_or_tomorrow_sunset(lat, lng)

        #finding appropriate forecast given sunset time
        #(we want the sunset time to be within the range of the forecast time)
        sunset_forecast = find_forecast(lst_of_forecast_dicts, sunset_datetime_obj)

        #adding the correctly ranged forecast to the final list
        sunset_forecasts.append(sunset_forecast)

    # #closest airport's forecast is the first one in the list!
    # closest_forecast = sunset_forecasts[0]


    return sunset_forecasts



#******************************************************************************#
#******************************************************************************#
#******************************************************************************#


if __name__ == '__main__':

    app = Flask(__name__)

    #connect to database
    connect_to_db(app)