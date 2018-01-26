#Sun Setup

Sun Setup uses the altitudes and amounts of clouds given by aviation weather
forecasts in order to generate a prediction about the sunset for any given
location as well as a recommendation of any nearby location that has a higher
rated sunset.

###Tech Stack

Python, Javascript, HTML/CSS, Flask, Bootstrap, jQuery, Jinja, 
Flask-SQLAlchemy, GeoAlchemy, PostgreSQL, PostGIS,
datetime, timezonefinder, pytz,
Google Maps API, CheckWX API, Sunrise-Sunset API

###Features

* uses JS Geolocation function to get browser coordinates
* Can also type in LAT/LNG, Google maps autocomplete address, or choose
 from favorite locations (if user is logged in) on the advanced search page.
* Also on advanced search page can change the distance that you're querying
* A user can also log in to add favorite locations and upload photos

###Example Storyline

We'll start with the homepage:
![Alt text](/screenshots/home.png?raw=true "Sun Setup Home")

