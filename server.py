"""Sunsets"""

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

    code = str(request.args.get('icao'))

    # airport_obj = Airport.query.filter(Airport.icao_code == code)
    airport_obj = Airport.query.filter(Airport.icao_code == code).one()


    return render_template('prediction.html', icao_code=code, airport_obj=airport_obj)




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





