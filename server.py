"""Sunsets"""

import os
#So that we can make jinja not yell at us
from jinja2 import StrictUndefined
import datetime

from sqlalchemy import func
from geoalchemy2 import Geography

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
from forecast import today_or_tomorrow_sunset, find_nearest_airport_forecast
# from forecast import find_forecast
from cloud_rating import make_cloud_dict, return_rating
from maps import get_coordinates_from_address

from errors import NoForecastDataError

UPLOAD_FOLDER = 'static/user_images/'


app = Flask(__name__)
#in order to use the debugging toolbar:
app.secret_key = 'kiloechoyankee'

#this makes jijnja yell at you for undefined variables
app.jinja_env.undefined = StrictUndefined

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    if 'current_user' in session:
        user_obj = User.query.get(session['current_user'])
    else:
        user_obj = None


    return render_template('location.html',
                           mapsapiurl=places_map_url,
                           placesmapurl=places_map_url,
                           user_obj=user_obj)


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

    elif 'favoritelocation' in request.args:
        favlocation = request.args.get('favoritelocation')
        #has to match user ID AND location title
        fav_location = UserFavorite.query.filter(UserFavorite.favorite_title == favlocation, UserFavorite.user_id == session['current_user']).one()
        user_lat = fav_location.favorite_lat
        user_lon = fav_location.favorite_lng

    elif 'usrlat' in request.args:
        user_lat = request.args.get('usrlat')
        user_lon = request.args.get('usrlng')
        print user_lat
        print type(user_lat)
        print user_lon
        print type(user_lon)


    else:
        print "something didn't work"
        flash("didn't work")
        return redirect('/location')

    user_point = 'POINT({} {})'.format(user_lon, user_lat)

    #Time of today or tomorrow's sunset
    #For display purposes:
    sunset_datetime_obj = today_or_tomorrow_sunset(user_lat, user_lon)

    #forecast containing weather information AND icao code (new and imporoved)
    #adding try and except for no airport error

    try:
        forecasts = find_nearest_airport_forecast(user_point)
    except:
        flash("I'm sorry! There are no available forecasts in this area =[ ")
        return redirect('/location')


    closest_forecast_json = forecasts[0]

    #**************************** RECOMENDATION *******************************#

    #Even the worst rating is higher than this number:
    highest_rating = -6000

    recomendation = None

    for forecast in forecasts:
        cat_cloud_dict = make_cloud_dict(forecast)
        rate_desc_dict = return_rating(cat_cloud_dict)
        rating = rate_desc_dict['value']
        if rating > highest_rating:
            highest_rating = rating
            recomendation = forecast['icao']
            print "RECOMENDATION"
            print recomendation
            rec_forecast = forecast
            print "SAME RECOMENDATION:"
            print rec_forecast['icao']
            print type(rec_forecast)
        else:
            print "{} did not have a better forecast".format(forecast['icao'])

    print recomendation, highest_rating

    if recomendation == closest_forecast_json['icao']:
        rec_message = """You've got the highest rated sunset in your area! \n
                        We recommend you stay right where you are! """
        rec_forecast = "same"

    else:
        rec_message = """{} has a higher rated sunset! \n
                        We reccomend you go there for the
                        best sunset experience.""".format(recomendation)
        print rec_forecast


    icao_code = closest_forecast_json['icao']
    #Querying for the airport with the code from the forecast
    airport_obj = Airport.query.filter(Airport.icao_code == icao_code).one()

    #for display purposes only
    current_utc = datetime.datetime.utcnow()

    #Making a specifcally formated cloud dictionary to use
    #in return rating (which returns a dictionary with rating and description)
    cat_cloud_dict = make_cloud_dict(closest_forecast_json)
    rate_desc_dict = return_rating(cat_cloud_dict)
    description = rate_desc_dict['description']


    return render_template('prediction.html',
                           icao_code=icao_code,
                           airport_obj=airport_obj,
                           sunset_time=sunset_datetime_obj,
                           forecast=closest_forecast_json,
                           current_utc=current_utc,
                           description=description,
                           userLat=user_lat,
                           userLon=user_lon,
                           mapsapiurl=maps_src_url,
                           rec_forecast=rec_forecast,
                           rec_message=rec_message)


#******************************************************************************#
#***************************** Login/Registration *****************************#
#******************************************************************************#


@app.route('/register')
def show_register_form():
    """Registration form"""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def process_form():
    """Process registration information"""

    user_name = request.form.get('name')
    user_email = request.form.get('email')
    user_pass = request.form.get('password')


    user_object = User.query.filter(User.user_email == user_email).first()

    if user_object:

        flash("You already have an account. Please log in!")
        return redirect('/login')
    #If user object with email address provided doens't exist, add to db...
    else:        
        new_user = User(user_name=user_name,
                        user_email=user_email,
                        user_pass=user_pass)

        db.session.add(new_user)
        db.session.commit()

    return redirect('/login')


@app.route('/login')
def login_page():
    """Page form for logging in user"""

    if 'current_user' in session:
        flash('You\'re already logged in...silly goose')
        return redirect('/')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """process login form, redirect to user's page when it works"""

    user_email = request.form.get('email')
    user_pass = request.form.get('password')

    user_object = User.query.filter(User.user_email == user_email).first()

    if user_object:

        if user_object.user_pass == user_pass:
            flash("You're logged in. Welcome!")
            specific_user_id = user_object.user_id
            session['current_user'] = specific_user_id

        else:
            flash("That is an incorrect password")
            return redirect('/login')

    else:
        flash('You need to register first!')

        return redirect('/register')


    return redirect('/')


@app.route('/logout')
def logout_user():
    """logs out user by deleting the current user from the session"""

    del session['current_user']
    flash('successfully logged out')
    return redirect ('/')

#******************************************************************************#
#******************************** User Routes *********************************#
#******************************************************************************#

@app.route('/mypage')
def users_page():
    """Displays user's favorites and photos"""

    if 'current_user' not in session:
        flash('Please log in to see your page!')
        return redirect('/')
    else:
        user_id = session['current_user']
        user_obj = User.query.get(user_id)
        print user_obj.favorites

        return render_template('mypage.html', user_obj=user_obj)


# ******************************* FAVORITES ***********************************#

@app.route('/addfavorite')
def get_favorite():
    """Form for adding a favorite location"""

    return render_template('addfavorite.html', placesmapurl=places_map_url)


@app.route('/addfavorite', methods=['POST'])
def add_favorite():
    """process login form, redirect to user's page when it works"""

    # NEED TO PUT API CHECK IN HERE FOR ADDRESS ASSOCIATION
    # ^^ what?? ^^

    #Getting the information the user has entered for favorite location
    favorite_location = request.form.get('address')
    favorite_title = request.form.get('title')

    #Getting lat and lng from the user's desired favorite location
    coordinates = get_coordinates_from_address(favorite_location)
    fav_lat = coordinates['lat']
    fav_lng = coordinates['lng']

    #making this into a point so we can compare distances
    fav_point = 'POINT({} {})'.format(fav_lng, fav_lat)

    #finding the nearest airport that has an available forecast:
    #Try and except incase there are no airports in range!

    try:
        nearest_airport_forecast = find_nearest_airport_forecast(fav_point)

    except:
        flash("I'm sorry! This location is too far from anywhere with available forecasts =[ ")
        return redirect("/addfavorite")

    closest_airport = nearest_airport_forecast[0]
    nearest_icao_code = closest_airport['icao']

    #Getting airport object for airport ID (to add to db)
    nearest_airport = Airport.query.filter(Airport.icao_code == nearest_icao_code).one()

    airport_id = nearest_airport.airport_id

    #instantiating new favorite object:
    new_favorite = UserFavorite(favorite_title=favorite_title,
                                favorite_lat=fav_lat,
                                favorite_lng=fav_lng,
                                favorite_location=fav_point,
                                airport_id=airport_id,
                                user_id=session['current_user'])

    db.session.add(new_favorite)
    db.session.commit()

    flash('{} added to your favorites!'.format(favorite_title))


    return redirect('/mypage')


# ********************************** PHOTOS ***********************************#

@app.route('/uploadphoto')
def upload_photo_form():
    """Form to upload a photo"""

    return render_template('uploadphoto.html', placesmapurl=places_map_url)


@app.route('/uploadphoto', methods=['POST'])
def upload_photo():
    """Uploads photo"""

    #getting information about the photo from the form:
    location = request.form.get('location')
    date = request.form.get('date')
    description = request.form.get('description')
    title = request.form.get('title')
    rating = request.form.get('rating')

    image = request.files['img']
    path_name = "usrid={}-{}-{}".format(session['current_user'], date, image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], path_name))
    ###### COME UP WITH BETTER FILE NAME #######
    image_path = app.config['UPLOAD_FOLDER'] + path_name
 

    #making date into object so we can add to DB:
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

    #Turning the location into a point for DB:
    coordinates = get_coordinates_from_address(location)
    photo_lat = coordinates['lat']
    photo_lng = coordinates['lng']
    photo_pt = 'POINT({} {})'.format(photo_lng, photo_lat)

    #finding nearest available airport so we can store that in db:
    nearest_airport_forecast = find_nearest_airport_forecast(photo_pt)
    nearest_icao_code = nearest_airport_forecast['icao']

    #Getting airport object for airport ID (to add to db)
    nearest_airport = Airport.query.filter(Airport.icao_code == nearest_icao_code).one()

    airport_id = nearest_airport.airport_id

    #using ST_Distance_Sphere gives units in meters instead of other weird something.
    #Distance is in METERS
    distance = db.session.query(func.ST_Distance_Sphere(func.ST_GeomFromText(photo_pt, 4326), 
                                                 nearest_airport.location)).one()[0]

    print photo_lat, photo_lng
    print nearest_airport.lattitude, nearest_airport.longitude
    print '**************'
    print distance
    print '**************'
    print type(distance)



    new_photo = Photo(user_id=session['current_user'],
                      airport_id=airport_id,
                      photo_title=title,
                      photo_lat=photo_lat,
                      photo_lng=photo_lng,
                      photo_location=photo_pt,
                      datetime=date_obj,
                      filepath=image_path,
                      airport_dist=distance,
                      sunset_rating=rating,
                      description=description)

    db.session.add(new_photo)
    db.session.commit()



    return redirect('/mypage')






#******************************************************************************#
#******************************************************************************#
#******************************************************************************#




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


