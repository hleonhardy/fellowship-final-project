"""Sunsets"""

import os
#So that we can make jinja not yell at us
from jinja2 import StrictUndefined
import datetime
from geoalchemy2.functions import ST_DWithin

from flask import (Flask,
                   render_template,
                   redirect, request,
                   flash,
                   session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Airport, UserFavorite, Photo
from model import connect_to_db, db

from checkwx import return_forecast_dict
from sunset_time import return_sunset_time
# from forecast import today_or_tomorrow_sunset, find_forecast
from cloud_rating import make_cloud_dict, return_rating
from maps import get_coordinates_from_address

from errors import NoForecastDataError


app = Flask(__name__)
#in order to use the debugging toolbar:
app.secret_key = 'kiloechoyankee'

#this makes jijnja yell at you for undefined variables
app.jinja_env.undefined = StrictUndefined

GOOGLE_MAPS_API_KEY = os.environ['GOOGLEMAPSAPIKEY']
maps_src_url = "https://maps.googleapis.com/maps/api/js?key={}&callback=initMap".format(GOOGLE_MAPS_API_KEY)
places_map_url = "https://maps.googleapis.com/maps/api/js?key={}&libraries=places&callback=initAutocomplete".format(GOOGLE_MAPS_API_KEY)


@app.route('/')
def index():
    """homepage"""

    return render_template('homepage.html')


@app.route('/location')
def get_prediction():
    """Form for entering location (for now)"""

    return render_template('location.html',
                           mapsapiurl=places_map_url,
                           placesmapurl=places_map_url)


@app.route('/prediction')
def show_prediction():
    """Displays prediction (information for now)"""

    # code = request.args.get('icao')
    # #ICAO codes are 4 uppercase letters:
    # code = code.upper()

    if 'lat' in request.args:
        user_lat = request.args.get('lat')
        user_lon = request.args.get('lon')

    elif 'address' in request.args:
        address = request.args.get('address')
        coordinates = get_coordinates_from_address(address)
        user_lat = coordinates['lat']
        user_lon = coordinates['lng']

    user_point = 'POINT({} {})'.format(user_lon, user_lat)

# *****************************************************************************#
# COMMENTING THIS OUT TO USE TEST DATA (so that I dont make too many api reqs.)#
# *****************************************************************************#

    # #distance in meters
    # distance = 10000
    # #limit on number of rows we get back from the query
    # lim = 50

    # sql_args = {'user_point': user_point, 'dist': distance, 'lim':lim}

    # sql = """SELECT airport_id FROM airports
    #         WHERE ST_DWithin(location, :user_point, :dist)
    #         ORDER BY location
    #         LIMIT :lim"""

    # cursor = db.session.execute(sql, sql_args)
    # # import pdb; pdb.set_trace()
    # #For now, just having this here to display in the html

    #looping through all the airports in the SQL query
    #Until we get to one that has available forecast data
    # i = 0
    # while i < lim:

    #     #fetchone will grab the first airport id tuple and
    #     #take it out of the cursor.
    #     #That way if we do fetchone again, it will grab the next one
    #     airport_id = cursor.fetchone()

    #     # import pdb; pdb.set_trace()

    #     airport_obj = Airport.query.get(airport_id)
    #     # airport_obj = Airport.query.filter(ST_DWithin(Airport.location, user_point, distance)).all()
    #     # #Getting the airport object for the given code
    #     # # airport_obj = Airport.query.filter(Airport.icao_code == code).one()
    #     # airport_obj = airport_obj[0]

    #     lat = airport_obj.lattitude
    #     lon = airport_obj.longitude

    #     code = airport_obj.icao_code

    #     #From forecast.py:
    #     #Determine whether or not to use today or tomorrow's sunset
    #     #based on if the sunset has already passed
    #     sunset_datetime_obj = today_or_tomorrow_sunset(lat, lon)

    #     #Getting the forecast for that specific time
    #     # import pdb; pdb.set_trace()
    #     try:
    #         forecast_json = find_forecast(code, sunset_datetime_obj)
    #         print forecast_json
    #         break
    #     except:
    #         i += 1

#******************************************************************************#
# TESTING FOR KSFO:
#******************************************************************************#
    sunset_datetime = '2017-11-15 00:58:48'

    code = 'KSFO'

    sunset_datetime_obj = datetime.datetime.strptime(sunset_datetime,
                                                       '%Y-%m-%d %H:%M:%S')

    airport_obj = Airport.query.get(6532)
    print airport_obj

    forecast_json = {
                    u'clouds': 
                        [{u'base_feet_agl': 5000,
                        u'code': u'FEW',
                        u'text': u'Few'},
                        {u'base_feet_agl': 25000,
                        u'code': u'FEW',
                        u'text': u'Few'}],
                    u'timestamp':
                        {u'forecast_from': u'14-11-2017 @ 21:00Z',
                        u'forecast_to': u'15-11-2017 @ 08:00Z'}
                    }

    current_utc = datetime.datetime.utcnow()

    #Making a specifcally formated cloud dictionary to use
    #in return rating (which returns a dictionary with rating and description)
    cat_cloud_dict = make_cloud_dict(forecast_json)
    rate_desc_dict = return_rating(cat_cloud_dict)
    description =  rate_desc_dict['description']



    return render_template('prediction.html',
                           icao_code=code,
                           airport_obj=airport_obj,
                           sunset_time=sunset_datetime_obj,
                           forecast=forecast_json,
                           current_utc=current_utc,
                           description=description,
                           userLat=user_lat,
                           userLon=user_lon,
                           mapsapiurl=maps_src_url)


if __name__ == '__main__':

    app.debug = True
    #doesn't cache templates, etc in debug mode:
    app.jinja_env.auto_reload = app.debug

    #connect to database
    connect_to_db(app)

    #to use the debugging toolbar:
    DebugToolbarExtension(app)


    #host with 0's so we can run with vagrant
    app.run(port=5000, host='0.0.0.0')


