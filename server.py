"""Sunsets"""

import os
from model import User, Airport, UserFavorite, Photo
from model import connect_to_db, db
#So that we can make jinja not yell at us
from jinja2 import StrictUndefined

from flask import (Flask,
                   render_template,
                   redirect, request,
                   flash,
                   session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from checkwx import return_forecast_dict
from sunset_time import return_sunset_time
from forecast import today_or_tomorrow_sunset, find_forecast
import datetime
from geoalchemy2.functions import ST_DWithin
from errors import NoForecastDataError
from maps import get_coordinates_from_address


app = Flask(__name__)
#in order to use the debugging toolbar:
app.secret_key = 'kiloechoyankee'

#this makes jijnja yell at you for undefined variables
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    """homepage"""

    return render_template('homepage.html')


@app.route('/location')
def get_prediction():
    """Form for entering location (for now)"""

    return render_template('location.html')


@app.route('/prediction')
def show_prediction():
    """Displays prediction (information for now)"""

    # GOOGLE_MAPS_API_KEY = os.environ['GOOGLEMAPSAPIKEY']
    # maps_src_url = "https://maps.googleapis.com/maps/api/js?key={}&callback=initMap".format(GOOGLE_MAPS_API_KEY)

    # code = request.args.get('icao')
    # #ICAO codes are 4 uppercase letters:
    # code = code.upper()

    if 'address' in request.args:
        print "hello address"
    elif 'lat' in request.args:
        print "hello laTitude!"

    user_lat = request.args.get('lat')
    user_lon = request.args.get('lon')
    user_point = 'POINT({} {})'.format(user_lon, user_lat)

    #distance in meters
    distance = 10000
    #limit on number of rows we get back from the query
    lim = 50

    sql_args = {'user_point': user_point, 'dist': distance, 'lim':lim}

    sql = """SELECT airport_id FROM airports
            WHERE ST_DWithin(location, :user_point, :dist)
            ORDER BY location
            LIMIT :lim"""

    cursor = db.session.execute(sql, sql_args)
    # import pdb; pdb.set_trace()
    #For now, just having this here to display in the html
    current_utc = datetime.datetime.utcnow()

    #looping through all the airports in the SQL query
    #Until we get to one that has available forecast data
    i = 0
    while i < lim:

        #fetchone will grab the first airport id tuple and
        #take it out of the cursor.
        #That way if we do fetchone again, it will grab the next one
        airport_id = cursor.fetchone()

        # import pdb; pdb.set_trace()

        airport_obj = Airport.query.get(airport_id)
        # airport_obj = Airport.query.filter(ST_DWithin(Airport.location, user_point, distance)).all()
        # #Getting the airport object for the given code
        # # airport_obj = Airport.query.filter(Airport.icao_code == code).one()
        # airport_obj = airport_obj[0]

        lat = airport_obj.lattitude
        lon = airport_obj.longitude

        code = airport_obj.icao_code

        #From forecast.py:
        #Determine whether or not to use today or tomorrow's sunset
        #based on if the sunset has already passed
        sunset_datetime_obj = today_or_tomorrow_sunset(lat, lon)

        #Getting the forecast for that specific time
        # import pdb; pdb.set_trace()
        try:
            forecast_json = find_forecast(code, sunset_datetime_obj)
            print forecast_json
            break
        except:
            i += 1


    return render_template('prediction.html',
                           icao_code=code,
                           airport_obj=airport_obj,
                           sunset_time=sunset_datetime_obj,
                           forecast=forecast_json,
                           current_utc=current_utc)


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


