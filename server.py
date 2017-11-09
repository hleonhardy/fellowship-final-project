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

    code = request.args.get('icao')
    #ICAO codes are 4 uppercase letters:
    code = code.upper()

    #Getting the airport object for the given code
    airport_obj = Airport.query.filter(Airport.icao_code == code).one()

    lat = airport_obj.lattitude
    lon = airport_obj.longitude

    #For now, just having this here to display in the html
    current_utc = datetime.datetime.utcnow()

    #From forecast.py:
    #Determine whether or not to use today or tomorrow's sunset
    #based on if the sunset has already passed
    sunset_datetime_obj = today_or_tomorrow_sunset(lat, lon)
    #Getting the forecast for that specific time
    forecast_json = find_forecast(code, sunset_datetime_obj)



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


